#include <gxx/io/file.h>
#include <gxx/io/serial_port.h>
#include <fcntl.h>
#include <unistd.h>

#include <gxx/osutil/fd.h>

#include <termios.h>

namespace gxx
{
	namespace io
	{

		file::file() {}
		file::file(const char* path, uint8_t mode)
		{
			open(path, mode);
		}

		file::file(int fd) : file_like(fd) {}

		bool file::open(const char* path, uint8_t mode)
		{
			//uint16_t flags = O_CREAT | O_NOCTTY;
			uint16_t flags = O_CREAT | O_NOCTTY;
			if (mode == gxx::io::NotOpen) return false;
			if (mode & gxx::io::ReadWrite) flags |= O_RDWR;
			if (mode & gxx::io::ReadOnly) flags |= O_RDONLY;
			if (mode & gxx::io::WriteOnly) flags |= O_WRONLY;
			if (mode & gxx::io::Append) flags |= O_APPEND;
			if (mode & gxx::io::Truncate) flags |= O_TRUNC;
			fd = ::open(path, flags, 0666);
			_is_open = true;
			return true;
		}

		int file_like::close()
		{
			return ::close(fd);
		}

		ssize_t file_like::readData(char *data, size_t maxSize) {
			//dprln(m_fd);
			return ::read(fd, data, maxSize);
		}

		ssize_t file_like::writeData(const char *data, size_t maxSize) {
			return ::write(fd, data, maxSize);
		}


		/*void file::setFileDescriptor(int m_fd) {
			this->m_fd = m_fd;
		}

		void file::setPath(const std::string& path) {
			this->path = path;
		}*/

		int file_like::nonblock(bool en)
		{
			return gxx::osutil::nonblock(fd, en);
		}

		bool file_like::is_open()
		{
			return _is_open;
		}





		int serial_port_file::open(const char * path,
		                           unsigned int baud,
		                           gxx::serial::parity parity,
		                           gxx::serial::bytesize bytesize,
		                           gxx::serial::stopbits stopbits,
		                           gxx::serial::flowcontrol flowcontrol)
		{
			int ret;

			fd = ::open(path, O_RDWR | O_NOCTTY);
			if (fd < 0) {
				perror("serial::open");
				exit(0);
			}

			struct termios tattr, orig;
			ret = tcgetattr(fd, &orig);
			if (ret < 0) {
				perror("serial::tcgetattr");
				exit(0);
			}

			tattr = orig;  /* copy original and then modify below */

			/* input modes - clear indicated ones giving: no break, no CR to NL,
			   no parity check, no strip char, no start/stop output (sic) control */
			tattr.c_iflag &= ~(BRKINT | ICRNL | INPCK | ISTRIP | IXON);

			/* output modes - clear giving: no post processing such as NL to CR+NL */
			tattr.c_oflag &= ~(OPOST);

			/* control modes - set 8 bit chars */
			tattr.c_cflag |= (CS8);

			/* local modes - clear giving: echoing off, canonical off (no erase with
			   backspace, ^U,...),  no extended functions, no signal chars (^Z,^C) */
			tattr.c_lflag &= ~(ECHO | ICANON | IEXTEN | ISIG);

			/* control chars - set return condition: min number of bytes and timer */
			tattr.c_cc[VMIN] = 1; tattr.c_cc[VTIME] = 0; /* immediate - anything       */

			switch (parity) 
			{
				case gxx::serial::parity_none:
					tattr.c_cflag &= ~(PARENB);
					tattr.c_cflag &= ~(PARODD);
					break;
				
				case gxx::serial::parity_even:
					tattr.c_cflag |= (PARENB);
					tattr.c_cflag &= ~(PARODD);
					break;
				
				case gxx::serial::parity_odd:
					tattr.c_cflag |= (PARENB);
					tattr.c_cflag |= (PARODD);
					break;					
				
				default:
					PANIC_TRACED();
			}

			if (baud == 115200) {
				cfsetispeed(&tattr, B115200);
				cfsetospeed(&tattr, B115200);
			} else {
				PANIC_TRACED();
			}

			/* put terminal in raw mode after flushing */
			ret = tcsetattr(fd, TCSAFLUSH, &tattr);

			if (ret < 0) {
				perror("serial::tcsetattr");
				exit(0);
			}


			_is_open = true;
			return fd;
		}
	}

//	io::file cout(0);
//	io::file cin(1);
//	io::file crr(2);
}
