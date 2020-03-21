# encoding: utf-8
import argparse
import datetime
import os
import shutil
from enum import Enum
from glob import glob
import multiprocessing as mp
# from threading import Thread


class QMCMask2Type(Enum):
    TYPE_128 = 1
    TYPE_256 = 2


class QMCMask2:
    seed_map_128 = [
        0xc3, 0x4a, 0xd6, 0xca, 0x90, 0x67, 0xf7, 0x52,
        0xd8, 0xa1, 0x66, 0x62, 0x9f, 0x5b, 0x09, 0x00,

        0xc3, 0x5e, 0x95, 0x23, 0x9f, 0x13, 0x11, 0x7e,
        0xd8, 0x92, 0x3f, 0xbc, 0x90, 0xbb, 0x74, 0x0e,

        0xc3, 0x47, 0x74, 0x3d, 0x90, 0xaa, 0x3f, 0x51,
        0xd8, 0xf4, 0x11, 0x84, 0x9f, 0xde, 0x95, 0x1d,

        0xc3, 0xc6, 0x09, 0xd5, 0x9f, 0xfa, 0x66, 0xf9,
        0xd8, 0xf0, 0xf7, 0xa0, 0x90, 0xa1, 0xd6, 0xf3,

        0xc3, 0xf3, 0xd6, 0xa1, 0x90, 0xa0, 0xf7, 0xf0,
        0xd8, 0xf9, 0x66, 0xfa, 0x9f, 0xd5, 0x09, 0xc6,

        0xc3, 0x1d, 0x95, 0xde, 0x9f, 0x84, 0x11, 0xf4,
        0xd8, 0x51, 0x3f, 0xaa, 0x90, 0x3d, 0x74, 0x47,

        0xc3, 0x0e, 0x74, 0xbb, 0x90, 0xbc, 0x3f, 0x92,
        0xd8, 0x7e, 0x11, 0x13, 0x9f, 0x23, 0x95, 0x5e,

        0xc3, 0x00, 0x09, 0x5b, 0x9f, 0x62, 0x66, 0xa1,
        0xd8, 0x52, 0xf7, 0x67, 0x90, 0xca, 0xd6, 0x4a
    ]
    seed_map_256 = [
        0x77, 0x48, 0x32, 0x73, 0xDE, 0xF2, 0xC0, 0xC8, 0x95, 0xEC, 0x30, 0xB2, 0x51, 0xC3, 0xE1, 0xA0,
        0x9E, 0xE6, 0x9D, 0xCF, 0xFA, 0x7F, 0x14, 0xD1, 0xCE, 0xB8, 0xDC, 0xC3, 0x4A, 0x67, 0x93, 0xD6,
        0x28, 0xC2, 0x91, 0x70, 0xCA, 0x8D, 0xA2, 0xA4, 0xF0, 0x08, 0x61, 0x90, 0x7E, 0x6F, 0xA2, 0xE0,
        0xEB, 0xAE, 0x3E, 0xB6, 0x67, 0xC7, 0x92, 0xF4, 0x91, 0xB5, 0xF6, 0x6C, 0x5E, 0x84, 0x40, 0xF7,
        0xF3, 0x1B, 0x02, 0x7F, 0xD5, 0xAB, 0x41, 0x89, 0x28, 0xF4, 0x25, 0xCC, 0x52, 0x11, 0xAD, 0x43,
        0x68, 0xA6, 0x41, 0x8B, 0x84, 0xB5, 0xFF, 0x2C, 0x92, 0x4A, 0x26, 0xD8, 0x47, 0x6A, 0x7C, 0x95,
        0x61, 0xCC, 0xE6, 0xCB, 0xBB, 0x3F, 0x47, 0x58, 0x89, 0x75, 0xC3, 0x75, 0xA1, 0xD9, 0xAF, 0xCC,
        0x08, 0x73, 0x17, 0xDC, 0xAA, 0x9A, 0xA2, 0x16, 0x41, 0xD8, 0xA2, 0x06, 0xC6, 0x8B, 0xFC, 0x66,
        0x34, 0x9F, 0xCF, 0x18, 0x23, 0xA0, 0x0A, 0x74, 0xE7, 0x2B, 0x27, 0x70, 0x92, 0xE9, 0xAF, 0x37,
        0xE6, 0x8C, 0xA7, 0xBC, 0x62, 0x65, 0x9C, 0xC2, 0x08, 0xC9, 0x88, 0xB3, 0xF3, 0x43, 0xAC, 0x74,
        0x2C, 0x0F, 0xD4, 0xAF, 0xA1, 0xC3, 0x01, 0x64, 0x95, 0x4E, 0x48, 0x9F, 0xF4, 0x35, 0x78, 0x95,
        0x7A, 0x39, 0xD6, 0x6A, 0xA0, 0x6D, 0x40, 0xE8, 0x4F, 0xA8, 0xEF, 0x11, 0x1D, 0xF3, 0x1B, 0x3F,
        0x3F, 0x07, 0xDD, 0x6F, 0x5B, 0x19, 0x30, 0x19, 0xFB, 0xEF, 0x0E, 0x37, 0xF0, 0x0E, 0xCD, 0x16,
        0x49, 0xFE, 0x53, 0x47, 0x13, 0x1A, 0xBD, 0xA4, 0xF1, 0x40, 0x19, 0x60, 0x0E, 0xED, 0x68, 0x09,
        0x06, 0x5F, 0x4D, 0xCF, 0x3D, 0x1A, 0xFE, 0x20, 0x77, 0xE4, 0xD9, 0xDA, 0xF9, 0xA4, 0x2B, 0x76,
        0x1C, 0x71, 0xDB, 0x00, 0xBC, 0xFD, 0x0C, 0x6C, 0xA5, 0x47, 0xF7, 0xF6, 0x00, 0x79, 0x4A, 0x11
    ]

    def __init__(self, mask_type: QMCMask2Type):
        self.mask_type = mask_type

    def next_mask(self, index: int):
        if self.mask_type == QMCMask2Type.TYPE_128:
            if index > 0x7FFF:
                return self.seed_map_128[(index % 0x7FFF) & 0x7F]
            else:
                return self.seed_map_128[index & 0x7F]
        else:
            offset = index if index <= 0x7FFF else (index % 0x7FFF)
            return self.seed_map_256[(offset * offset + 27) & 0xFF]
            # return self.seed_map_256[(offset * offset + 80923 & 0xFF) & 0xFF]


class QMCMask:
    seed_map = [[0x4a, 0xd6, 0xca, 0x90, 0x67, 0xf7, 0x52],
                [0x5e, 0x95, 0x23, 0x9f, 0x13, 0x11, 0x7e],
                [0x47, 0x74, 0x3d, 0x90, 0xaa, 0x3f, 0x51],
                [0xc6, 0x09, 0xd5, 0x9f, 0xfa, 0x66, 0xf9],
                [0xf3, 0xd6, 0xa1, 0x90, 0xa0, 0xf7, 0xf0],
                [0x1d, 0x95, 0xde, 0x9f, 0x84, 0x11, 0xf4],
                [0x0e, 0x74, 0xbb, 0x90, 0xbc, 0x3f, 0x92],
                [0x00, 0x09, 0x5b, 0x9f, 0x62, 0x66, 0xa1]]

    def __init__(self):
        self.x = -1
        self.y = 8
        self.dx = 1
        self.index = -1

    def reset(self):
        self.__init__()

    def next_mask(self):
        ret = 0
        self.index += 1
        if self.x < 0:
            self.dx = 1
            self.y = (8 - self.y) % 8
            ret = 0xc3

        elif self.x > 6:
            self.dx = -1
            self.y = 7 - self.y
            ret = 0xd8
        else:
            ret = self.seed_map[self.y][self.x]

        self.x += self.dx
        if self.index == 0x8000 or (self.index > 0x8000 and (self.index + 1) % 0x8000 == 0):
            return self.next_mask()
        return ret


class QMCDecoder:

    def __init__(self):
        self.suffix_map = {'.qmc3': '.mp3', '.qmc0': '.mp3', '.qmcflac': '.flac'}
        self.output_dir = ""
        self.masker = QMCMask()
        self.masker2 = QMCMask2(QMCMask2Type.TYPE_128)

    def _decode(self, input_file: str):
        self.masker.reset()
        input_file_name = input_file.split('/')[-1]
        idx = input_file_name.rfind('.')
        name, suffix = input_file_name[:idx], input_file_name[idx:]
        with open(input_file, 'rb') as f:
            data = bytearray(f.read())
        for i in range(len(data)):
            data[i] ^= self.masker.next_mask()

        output_file = self.output_dir + "/" + name + self.suffix_map[suffix]
        if os.path.exists(output_file):
            os.remove(output_file)
        with open(output_file, 'wb') as f:
            f.write(data)

    def _decode2(self, index: int, input_file: str, output_dir: str):

        file_size = os.path.getsize(input_file)
        offset = int(file_size / os.cpu_count()) * index
        size_to_process = 0
        if (index + 1) == os.cpu_count():
            size_to_process = file_size - offset
        elif (index + 1) < os.cpu_count():
            size_to_process = int(file_size / os.cpu_count())

        print("In process %d, offset: %d, size: %d" % (index, offset, size_to_process))
        with open(input_file, 'rb') as rf:
            rf.seek(offset, 0)
            data = bytearray(rf.read(size_to_process))
        for i in range(len(data)):
            data[i] ^= self.masker2.next_mask(offset + i)

        output_file = self.output_dir + "/" + str(index)
        if os.path.exists(output_file):
            os.remove(output_file)
        with open(output_file, 'wb') as wf:
            # wf.seek(offset, 0)
            wf.write(data)
            wf.close()

    def process2(self, input_dirs: [], output_dir: str = None):
        input_files = []
        for path in input_dirs:
            path = os.path.abspath(path)
            if not os.path.exists(path):
                continue
            if os.path.isdir(path):
                input_files += filter(lambda x: any([x.endswith(suf) for suf in self.suffix_map]), glob(path + "/*.*"))
            else:
                input_files += [path]

        self.output_dir = output_dir if output_dir else os.path.abspath(os.curdir) + "/output"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        if not os.path.isdir(self.output_dir):
            print('output: [%s] is not a folder' % self.output_dir)
            exit()

        # os.rmdir(self.output_dir)
        shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir)

        # thread_pool = []
        process_pool = []
        file_num = 0
        for file in input_files:
            print('Decoding %s...' % file)

            input_file_name = file.split('/')[-1]
            idx = input_file_name.rfind('.')
            name, suffix = input_file_name[:idx], input_file_name[idx:]
            output_file = self.output_dir + "/" + name + self.suffix_map[suffix]
            if os.path.exists(output_file):
                os.remove(output_file)

            # thread_pool.clear()
            process_pool.clear()
            for i in range(os.cpu_count()):
                process = mp.Process(target=QMCDecoder._decode2, args=(self, i, file, self.output_dir))
                process_pool.append(process)
                process.start()
                # thread = Thread(target=QMCDecoder._decode2, args=(self, i, file, output_file))
                # thread_pool.append(thread)
                # thread.start()

            for i in range(os.cpu_count()):
                process_pool[i].join()
                # thread_pool[i].join()

            tmp_files = os.listdir(self.output_dir)
            tmp_files.sort()
            of = open(output_file, 'wb')
            for tmp_file in tmp_files:
                tmp_path = self.output_dir + "/" + tmp_file
                print("Merging file: %s" % tmp_path)
                rf = open(tmp_path, 'rb')
                of.write(rf.read())
                rf.close()
                # os.remove(tmp_path)
            of.close()
            file_num += 1
            print("File: %s decoded successfully!" % file)
        print("Total %d files processed!" % file_num)

    def _decode3(self, index: int, input_file: str, sa):

        file_size = os.path.getsize(input_file)
        offset = int(file_size / os.cpu_count()) * index
        size_to_process = 0
        if (index + 1) == os.cpu_count():
            size_to_process = file_size - offset
        elif (index + 1) < os.cpu_count():
            size_to_process = int(file_size / os.cpu_count())

        print("In process %d, offset: %d, size: %d" % (index, offset, size_to_process))
        with open(input_file, 'rb') as rf:
            rf.seek(offset, 0)
            data = bytearray(rf.read(size_to_process))
        for i in range(len(data)):
            sa[offset + i] = self.masker2.next_mask(offset + i) ^ data[i]

        # for i in range(size_to_process):
        #     sa[offset + i] ^= self.masker2.next_mask(offset + i)

    def process3(self, input_dirs: [], output_dir: str = None):
        input_files = []
        for path in input_dirs:
            path = os.path.abspath(path)
            if not os.path.exists(path):
                continue
            if os.path.isdir(path):
                input_files += filter(lambda x: any([x.endswith(suf) for suf in self.suffix_map]), glob(path + "/*.*"))
            else:
                input_files += [path]

        self.output_dir = output_dir if output_dir else os.path.abspath(os.curdir) + "/output"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        if not os.path.isdir(self.output_dir):
            print('output: [%s] is not a folder' % self.output_dir)
            exit()

        shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir)

        process_pool = []
        file_num = 0
        for file in input_files:
            print('Decoding %s...' % file)

            input_file_name = file.split('/')[-1]
            idx = input_file_name.rfind('.')
            name, suffix = input_file_name[:idx], input_file_name[idx:]
            output_file = self.output_dir + "/" + name + self.suffix_map[suffix]
            if os.path.exists(output_file):
                os.remove(output_file)

            process_pool.clear()
            rf = open(file, 'rb')
            #RawArray不带同步机制（锁）
            sa = mp.RawArray('B', os.path.getsize(file))
            # sa = mp.RawArray('B', bytearray(rf.read()))
            #Array默认默认带同步机制（锁）
            # sa = mp.Array('B', os.path.getsize(file))
            rf.close()

            for i in range(os.cpu_count()):
                process = mp.Process(target=QMCDecoder._decode3, args=(self, i, file, sa))
                process_pool.append(process)
                process.start()

            for i in range(os.cpu_count()):
                process_pool[i].join()

            of = open(output_file, 'wb')
            of.write(sa)
            of.close()
            file_num += 1
            print("File: %s decoded successfully!" % file)
        print("Total %d files processed!" % file_num)

    def process(self, input_dirs: [], output_dir: str = None):
        input_files = []
        for path in input_dirs:
            path = os.path.abspath(path)
            if not os.path.exists(path):
                continue
            if os.path.isdir(path):
                input_files += filter(lambda x: any([x.endswith(suf) for suf in self.suffix_map]), glob(path + "/*.*"))
            else:
                input_files += [path]

        self.output_dir = output_dir if output_dir else os.path.abspath(os.curdir) + "/output"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        if not os.path.isdir(self.output_dir):
            print('output: [%s] is not a folder' % self.output_dir)
            exit()

        file_num = 0
        for file in input_files:
            print('Decoding %s...' % file)
            self._decode(file)
            file_num += 1
            print("File: %s decoded successfully!" % file)
        print("Total %d files processed!" % file_num)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Online music file of protected format decoder")
    parser.add_argument('input', nargs='*', default=['.'],
                        help='input directorie[s] containing protected music files')
    parser.add_argument('-o', '--output', default=None,
                        help='output dir, default will create /output dir under input path')
    parser.add_argument('-m', '--multi_processing', default=False, action="store_true",
                        help='Enable multi_processing mode')

    args = parser.parse_args()
    qmc = QMCDecoder()
    start_time = datetime.datetime.now()
    # if args.multi_threaded:
    if args.multi_processing:
        # qmc.process2(args.input, args.output)
        qmc.process3(args.input, args.output)
    else:
        qmc.process(args.input, args.output)
    end_time = datetime.datetime.now()
    time_cost = (end_time - start_time).seconds
    print("Total processing time: %d seconds!" % time_cost)
