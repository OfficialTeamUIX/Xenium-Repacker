# Xenium-Repacker
This simple script will take a XeniumOS image dump as input, and separate it to its individual core components. This script was put together to work with different components of a XeniumOS flash image, for experimentation on how the chip works with those components. Information was taken from Ryzee's OpenXenium CPLD code to identify where things were within the flash layout.

You can use this script to extract, or rebuild an image that can be restored via xenium-tools.

It is not recommended to change the recovery image, ever. Like, ever. We have no warranty and will not be held liable for any damages caused to you, your console, or in the random event you cat spontaneously combusts (Sorry Steve.)

Example Usage (testing):
Extract a flash image, drop in a testing version of Cromwell (or the RTOS bootloader), rebuild. Test your new image.
