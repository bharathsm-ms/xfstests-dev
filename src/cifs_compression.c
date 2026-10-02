#include <errno.h>
#include <fcntl.h>
#include <linux/fs.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/stat.h>
#include <unistd.h>

static void fail(const char *operation)
{
	perror(operation);
	exit(1);
}

static void require(int condition, const char *message)
{
	if (!condition) {
		fprintf(stderr, "%s\n", message);
		exit(1);
	}
}

static void check_flags(int descriptor, int compressed)
{
	int flags = 0;
	struct stat metadata;

	if (fstat(descriptor, &metadata) ||
	    ioctl(descriptor, FS_IOC_GETFLAGS, &flags))
		fail("read compression flags");
	require(!!(flags & FS_COMPR_FL) == compressed,
		"compression flag did not match requested state");
}

int main(int argc, char **argv)
{
	unsigned char payload[65536], actual[65536];
	int descriptor, writer = -1, result, expected_error = 0;
	int probe, writable, borrowed;
	int flags;
	size_t index;

	if (argc != 3) {
		fprintf(stderr, "usage: %s path probe|probe-writable|writable|borrowed|unlinked|noserverino\n", argv[0]);
		return 1;
	}
	probe = !strcmp(argv[2], "probe") || !strcmp(argv[2], "probe-writable");
	writable = !strcmp(argv[2], "writable") || !strcmp(argv[2], "probe-writable");
	borrowed = !strcmp(argv[2], "borrowed");
	if (!strcmp(argv[2], "unlinked"))
		expected_error = ESTALE;
	else if (!strcmp(argv[2], "noserverino"))
		expected_error = EOPNOTSUPP;
	require(probe || writable || borrowed || expected_error, "unknown mode");

	for (index = 0; index < sizeof(payload); index++)
		payload[index] = index % 251;
	descriptor = open(argv[1], O_CREAT | O_EXCL | O_RDWR, 0600);
	if (descriptor < 0)
		fail("create fixture");
	require(write(descriptor, payload, sizeof(payload)) == sizeof(payload),
		"short fixture write");
	if (fsync(descriptor))
		fail("fsync fixture");
	if (!writable) {
		if (borrowed)
			writer = descriptor;
		else if (close(descriptor))
			fail("close writable handle");
		descriptor = open(argv[1], O_RDONLY);
		if (descriptor < 0)
			fail("open read-only handle");
	}
	if (expected_error == ESTALE && unlink(argv[1]))
		fail("unlink open fixture");

	flags = FS_COMPR_FL;
	result = ioctl(descriptor, FS_IOC_SETFLAGS, &flags);
	if (probe && result < 0 && (errno == EOPNOTSUPP || errno == ENOTTY)) {
		perror("compression probe unsupported");
		return 77;
	}
	if (expected_error) {
		require(result == -1 && errno == expected_error,
			"compression fallback returned the wrong error");
	} else {
		if (result)
			fail("enable compression");
		check_flags(descriptor, 1);
		flags = 0;
		if (ioctl(descriptor, FS_IOC_SETFLAGS, &flags))
			fail("disable compression");
		check_flags(descriptor, 0);
		flags = FS_NODUMP_FL;
		result = ioctl(descriptor, FS_IOC_SETFLAGS, &flags);
		require(result == -1 && errno == EOPNOTSUPP,
			"unsupported file flag was not rejected");
		check_flags(descriptor, 0);
	}
	require(pread(descriptor, actual, sizeof(actual), 0) == sizeof(actual),
		"short verification read");
	require(!memcmp(actual, payload, sizeof(payload)), "file data changed");
	if (close(descriptor) || (writer >= 0 && close(writer)))
		fail("close fixture");
	return 0;
}
