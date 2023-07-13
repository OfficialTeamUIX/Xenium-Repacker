import os
import sys
import argparse

# Define the size of the full image in bytes
FULL_IMAGE_SIZE = 2 * 1024 * 1024  # 2MB

def disassemble_image(image_path, bank_data):
    with open(image_path, "rb") as f:
        image_data = f.read()

    # Create a directory to store the extracted banks
    output_dir = "extracted_banks"
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over the bank information and extract the banks
    for bank_name, start_offset, end_offset in sorted(bank_data, key=lambda x: x[1]):
        # Calculate the bank size based on the address offsets
        bank_size = end_offset - start_offset + 1

        # Extract the bank data from the image
        bank_data = image_data[start_offset : end_offset + 1]

        # Save the bank data to a file
        output_filename = f"{output_dir}/{bank_name}.bin"
        with open(output_filename, "wb") as bank_file:
            bank_file.write(bank_data)

        # Print the bank information
        print(f"Extracted {bank_name} (Size: {bank_size // 1024} KB) to {output_filename}")

    # Print the total size of the image
    total_size = len(image_data)
    print(f"Total image size: {total_size // 1024} KB")

def re_assemble_image(input_dir, output_image_path, bank_data):
    # Create a list to hold the image data
    image_data = bytearray()

    # Sort the bank data based on the start offset
    sorted_bank_data = sorted(bank_data, key=lambda x: x[1])

    for bank_name, start_offset, end_offset in sorted_bank_data:
        # Calculate the bank size based on the address offsets
        bank_size = end_offset - start_offset + 1

        # Check if we need to pad the image data with zeroes
        if len(image_data) < start_offset:
            # Calculate the number of zeroes needed
            padding_size = start_offset - len(image_data)

            # Pad the image data with zeroes
            image_data += bytearray(padding_size)

        # Open the bank file and read the bank data
        input_filename = f"{input_dir}/{bank_name}.bin"
        with open(input_filename, "rb") as bank_file:
            bank_data = bank_file.read()

        # Append the bank data to the image data
        image_data += bank_data

        # Print the bank information
        print(f"Re-assembled {bank_name} (Size: {bank_size // 1024} KB) from {input_filename}")

    # Pad the image data to the full size with zeroes
    if len(image_data) < FULL_IMAGE_SIZE:
        # Calculate the number of zeroes needed
        padding_size = FULL_IMAGE_SIZE - len(image_data)

        # Pad the image data with zeroes
        image_data += bytearray(padding_size)

    # Save the image data to a file
    with open(output_image_path, "wb") as f:
        f.write(image_data)

    # Print the total size of the re-assembled image
    total_size = len(image_data)
    print(f"Total re-assembled image size: {total_size // 1024} KB")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Disassemble and re-assemble image files.')
    parser.add_argument('image_path', help='Path to the input image file for disassembly, or output image file for re-assembly.')
    parser.add_argument('-d', '--disassemble', action='store_true', help='Disassemble the input image file.')
    parser.add_argument('-p', '--pack', action='store_true', help='Re-assemble the image file from the extracted banks.')
    parser.add_argument('-i', '--input', default='extracted_banks', help='Path to the input directory for re-assembly.')

    args = parser.parse_args()

    # Bank data: [Bank Name, Start Offset, End Offset]
    # This is working as of right now, but information COULD be incorrect. Always TBV (Trust but Verify)
    bank_data = [
        ["Recovery", 0x1C0000, 0x1DFFFF],  # 128KB within Bank 10 (Recovery)
        ["XeniumOS_Additional_Data", 0x1E0000, 0x1FBFFF],  # Additional XeniumOS Data (Bios banks)
        ["EEPROM_Backup_XeniumOS_Settings", 0x1FC000, 0x1FFFFF],  # EEPROM backup and XeniumOS settings
        ["Cromwell", 0x180000, 0x1BFFFF],  # 256KB within Bank 1 (Cromwell/RTOS)
        ["XeniumOS", 0x100000, 0x17FFFF],  # 512KB within Bank 2 (XeniumOS Data)
    ]

    if args.disassemble:
        disassemble_image(args.image_path, bank_data)
    elif args.pack:
        re_assemble_image(args.input, args.image_path, bank_data)
    else:
        print("Either --disassemble (-d) or --pack (-p) must be specified.")
