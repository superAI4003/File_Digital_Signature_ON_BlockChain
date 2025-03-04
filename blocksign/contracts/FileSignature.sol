// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract FileSignature {
    struct FileRecord {
        address signer;    // The person who signed the file
        bytes signature;   // Digital signature
        uint256 timestamp; // Time of signing
    }

    // Mapping of file hashes to an array of FileRecords
    mapping(bytes32 => FileRecord[]) public records;

    event FileSigned(address indexed signer, bytes32 fileHash, uint256 timestamp);

    // Function to store file signature
    function signFile(bytes32 fileHash, bytes memory signature) public {
        // Check if the sender has already signed the file
        for (uint i = 0; i < records[fileHash].length; i++) {
            require(records[fileHash][i].signer != msg.sender, "File already signed by this user");
        }

        records[fileHash].push(FileRecord({
            signer: msg.sender,
            signature: signature,
            timestamp: block.timestamp
        }));

        emit FileSigned(msg.sender, fileHash, block.timestamp);
    }

    function verifyFile(bytes32 fileHash, address user) public view returns (address, bytes memory, uint256) {
        require(records[fileHash].length > 0, "File not signed");
        for (uint i = 0; i < records[fileHash].length; i++) {
            if (records[fileHash][i].signer == user) {
                FileRecord memory record = records[fileHash][i];
                return (record.signer, record.signature, record.timestamp);
            }
        }
        revert("File not signed");
    }

}