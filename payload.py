from resources import *
from installer import *
import update_metadata_pb2
import shutil
import struct
from zipfile import ZipFile
import threading
import os
import os.path
import platform

# Global variables
vec = pygame.math.Vector2

def vec_to_int(vector):
    return int(vector.x), int(vector.y)

def write_json () :
    data = json.dumps(device_partitions)
    with open('partitions.json', 'w') as save:
        save.write(data)

PROGRAMS = [ 'bzcat', 'xzcat' ]

BRILLO_MAJOR_PAYLOAD_VERSION = 2

class PayloadError(Exception):
  pass


class Payload(object):

    class _PayloadHeader(object):
        _MAGIC = b'CrAU'

        def __init__(self):
          self.version = None
          self.manifest_len = None
          self.metadata_signature_len = None
          self.size = None

        def ReadFromPayload(self, payload_file):
          magic = payload_file.read(4)
          if magic != self._MAGIC:
            raise PayloadError('Invalid payload magic: %s' % magic)
          self.version = struct.unpack('>Q', payload_file.read(8))[0]
          self.manifest_len = struct.unpack('>Q', payload_file.read(8))[0]
          self.size = 20
          self.metadata_signature_len = 0
          if self.version != BRILLO_MAJOR_PAYLOAD_VERSION:
            raise PayloadError('Unsupported payload version (%d)' % self.version)
          self.size += 4
          self.metadata_signature_len = struct.unpack('>I', payload_file.read(4))[0]

    def __init__(self, payload_file) :
        pygame.init()
        self.running = True
        self.screen = WIN
        self.rect = self.screen.get_rect()
        self.mouse = vec()
        self.mouse_visible = True
        self.clock = pygame.time.Clock()
        self.magic =  b'CrAU'
        self.partition_name = ''
        self.extract_payload = True
        self.header = None
        self.manifest = None
        self.data_offset = None
        self.metadata_signature = None
        self.metadata_size = None
        self.payload_file = payload_file
        self.output = ''
        self.partitions_list = []

    def draw_extracting_window(self) :

        while self.extract_payload :
            
            self.screen.fill(BLACK)
            self.screen.blit(smartphone_bg, (120, -150))
            self.screen.blit(animation_485, (-10, -80))
            dialog = small_font.render("Extracting %s" % self.partition_name, 1, WHITE)
            self.screen.blit(dialog, (560, 450))

            if not self.extract_payload :
                self.screen.fill(BLACK)
                self.screen.blit(smartphone_bg, (120, -150))
                self.screen.blit(animation_485, (-10, -80))
                dialog = small_font.render("Everything ready!", 1, WHITE)
                self.screen.blit(dialog, (560, 450))

            pygame.display.update()

    def _ReadManifest(self):
        return self.payload_file.read(self.header.manifest_len)

    def _ReadMetadataSignature(self):
        self.payload_file.seek(self.header.size + self.header.manifest_len)
        return self.payload_file.read(self.header.metadata_signature_len);

    def ReadDataBlob(self, offset, length):
        self.payload_file.seek(self.data_offset + offset)
        return self.payload_file.read(length)

    def Init(self, output, payload):
        self.header = self._PayloadHeader()
        self.header.ReadFromPayload(self.payload_file)
        manifest_raw = self._ReadManifest()
        self.manifest = update_metadata_pb2.DeltaArchiveManifest()
        self.manifest.ParseFromString(manifest_raw)
        metadata_signature_raw = self._ReadMetadataSignature()
        if metadata_signature_raw:
          self.metadata_signature = update_metadata_pb2.Signatures()
          self.metadata_signature.ParseFromString(metadata_signature_raw)
        self.metadata_size = self.header.size + self.header.manifest_len
        self.data_offset = self.metadata_size + self.header.metadata_signature_len

        # Create new threads
        self.output = output

        thread_1 = threading.Thread(target=self.draw_extracting_window, name="ui")
        thread_2 = threading.Thread(target=self.controller_screen, name="ui")
        thread_3 = threading.Thread(target=self.extracting_payload, name="payload", args=([payload, output]))

        # Start threads
        thread_1.start()
        thread_2.start()
        thread_3.start()

        start = self.controller_screen()

        # Wait for all threads to end
        while self.extract_payload :
            thread_1.join()
            thread_2.join()
            thread_3.join()

        installer = Installer()
        installer.start_install()

    def decompress_payload(self, command, data, size, hash):
        if platform.system() == "Windows" :
            p = subprocess.Popen(['binaries/'+command+'.exe', '-'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)

        else :
            p = subprocess.Popen([command, '-'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)

        r = p.communicate(data)[0]
        
        return r

    def parse_payload(self, payload_f, partition, output):
      BLOCK_SIZE = 4096
      for operation in partition.operations:
        e = operation.dst_extents[0]
        data = payload_f.ReadDataBlob(operation.data_offset, operation.data_length)
        output.seek(e.start_block * BLOCK_SIZE)
        if operation.type == update_metadata_pb2.InstallOperation.REPLACE:
          output.write(data)
        elif operation.type == update_metadata_pb2.InstallOperation.REPLACE_XZ:
          r = self.decompress_payload('xzcat', data, e.num_blocks * BLOCK_SIZE, operation.data_sha256_hash)
          output.write(r)
        elif operation.type == update_metadata_pb2.InstallOperation.REPLACE_BZ:
          r = self.decompress_payload('bzcat', data, e.num_blocks * BLOCK_SIZE, operation.data_sha256_hash)
          output.write(r)
        elif operation.type == update_metadata_pb2.InstallOperation.ZERO:
          output.write(b'\x00' * (e.num_blocks * BLOCK_SIZE))
        else:
          raise PayloadError('Unhandled operation type ({} - {})'.format(operation.type,
                             update_metadata_pb2.InstallOperation.Type.Name(operation.type)))

    def extracting_payload(self, payload, output) :

        # Extracting all partitions from payload
        for partition in payload.manifest.partitions :
            self.partition_name = partition.partition_name  + '.img'
            output_img = open(os.path.join(output, self.partition_name),'wb+')
            out = output + '/' + self.partition_name

            self.partitions_list.append(self.partition_name)

            try :
                self.parse_payload(payload, partition, output_img)
                # Add the partitions to an external JSON file
                device_partitions["PARTITIONS"] = self.partitions_list
                write_json()

            except PayloadError as e:
                print('Failed: %s' % e)
                output_img.close()

        self.extract_payload = False

    def check_click(self, mouse) :
        print("Extracting...")


    def controller_screen(self) :

        while self.extract_payload :

            for event in pygame.event.get() :

                if event == pygame.QUIT :
                    self.running = False

                elif event == pygame.MOUSEBUTTONDOWN :
                    self.check_click(event.pos)


def start_extraction() :
    # Create output dir
    output = 'downloads' + '/' + oneplus_app_data["CURRENT_DEVICE"]["NAME"] + '/' + 'output'

    try :
        os.mkdir(output)

    except FileExistsError as error :
        shutil.rmtree(output)
        os.mkdir(output)


    # Extract the OTA file
    path = oneplus_app_data["CURRENT_DEVICE"]["NAME"]
    path =  'downloads' + '/' + path + '/' + 'ota.zip'
    ota_file = ZipFile(path)
    payload = open(ota_file.extract('payload.bin', output ), 'rb')


    # Update payload file
    payload = Payload(payload)
    payload.Init(output, payload)




