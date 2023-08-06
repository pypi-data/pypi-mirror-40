
# Capabilities in this module will only
# be made available if you have fusepy installed.

# sudo pip3 install fusepy

# We can return errors by raising
# OSError(number, 'unused description')
# where number comes from these header files
# https://github.com/torvalds/linux/blob/master/include/uapi/asm-generic/errno.h
# https://github.com/torvalds/linux/blob/master/include/uapi/asm-generic/errno-base.h

from __future__ import with_statement

import os
import sys
import errno
import stat
import time

import bb_unsucked

from fuse import FUSE, FuseOSError, Operations


class BBFS(Operations):
    def __init__(self, bb_unsucked_instance):
        self.bb = bb_unsucked_instance

    # # Filesystem methods
    # # ==================

    # def access(self, path, mode):
    #     full_path = self._full_path(path)
    #     if not os.access(full_path, mode):
    #         raise FuseOSError(errno.EACCES)

    # def chmod(self, path, mode):
    #     full_path = self._full_path(path)
    #     return os.chmod(full_path, mode)

    # def chown(self, path, uid, gid):
    #     full_path = self._full_path(path)
    #     return os.chown(full_path, uid, gid)

    def getattr(self, path, fh=None):
        parent_path = os.path.dirname(path)
        base_name = os.path.basename(path)
        now_s = int(time.time())
        attributes = {
          'st_atime': now_s, # last access time
          'st_ctime': now_s, # last status change time
          'st_gid': os.getgid(),   # group id of owner
          # See https://jameshfisher.com/2017/02/24/what-is-mode_t.html
          'st_mode': stat.S_IFDIR,
          
          'st_mtime': now_s,
          'st_nlink': 1, # number of hard links
          'st_size': 10, # total size in bytes
          'st_uid': os.getuid()
        }
        # Modify defaults based on path, basename
        if parent_path == "/":
          attributes['st_mode'] = stat.S_IFDIR
          attributes['st_size'] = 0
        
        return attributes

    def readdir(self, path, fh):
        parent_path = os.path.dirname(path)
        base_name = os.path.basename(path)
        print(path+"   "+parent_path+"     "+base_name)
        dirents = ['.', '..']
        if len(path) < 2: # == "/"
          for c in self.bb.classes():
            if c.is_current():
              dirents.append(c.file_name())
            else:
              dirents.append("."+c.file_name())
        elif parent_path == "/":
          # path != "/", this is a class, list it's contents
          class_id = base_name.split("_")[0]
          clazz = self.bb.fuzzy_class_by_course_id(class_id)
          if not clazz:
            raise OSError(2, "no such class")
          links = clazz.get_sidebar_links(self.bb.session, self.bb.get_cookies())
          for link in links:
            #dirents.append(path+"/"+link["text"])
            dirents.append(
              bb_unsucked.sanitize_for_use_in_filesystem(link["text"])
            )
          
        for r in dirents:
           yield r

    # def readlink(self, path):
    #     pathname = os.readlink(self._full_path(path))
    #     if pathname.startswith("/"):
    #         # Path name is absolute, sanitize it.
    #         return os.path.relpath(pathname, self.root)
    #     else:
    #         return pathname

    # def mknod(self, path, mode, dev):
    #     return os.mknod(self._full_path(path), mode, dev)

    # def rmdir(self, path):
    #     full_path = self._full_path(path)
    #     return os.rmdir(full_path)

    # def mkdir(self, path, mode):
    #     return os.mkdir(self._full_path(path), mode)

    # def statfs(self, path):
    #     full_path = self._full_path(path)
    #     stv = os.statvfs(full_path)
    #     return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
    #         'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
    #         'f_frsize', 'f_namemax'))

    # def unlink(self, path):
    #     return os.unlink(self._full_path(path))

    # def symlink(self, name, target):
    #     return os.symlink(name, self._full_path(target))

    # def rename(self, old, new):
    #     return os.rename(self._full_path(old), self._full_path(new))

    # def link(self, target, name):
    #     return os.link(self._full_path(target), self._full_path(name))

    # def utimens(self, path, times=None):
    #     return os.utime(self._full_path(path), times)

    # File methods
    # ============

    # def open(self, path, flags):
    #     full_path = self._full_path(path)
    #     return os.open(full_path, flags)

    # def create(self, path, mode, fi=None):
    #     full_path = self._full_path(path)
    #     return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    # def read(self, path, length, offset, fh):
    #     raise OSError(25, 'not a typewriter')
    #     os.lseek(fh, offset, os.SEEK_SET)
    #     return os.read(fh, length)

    # def write(self, path, buf, offset, fh):
    #     os.lseek(fh, offset, os.SEEK_SET)
    #     return os.write(fh, buf)

    # def truncate(self, path, length, fh=None):
    #     full_path = self._full_path(path)
    #     with open(full_path, 'r+') as f:
    #         f.truncate(length)

    # def flush(self, path, fh):
    #     return os.fsync(fh)

    # def release(self, path, fh):
    #     return os.close(fh)

    # def fsync(self, path, fdatasync, fh):
    #     return self.flush(path, fh)


def main(mountpoint, bb_unsucked_instance):
    FUSE(BBFS(bb_unsucked_instance), mountpoint, nothreads=True, foreground=True)




