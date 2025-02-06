// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract FileSignature {
    struct FileRecord {
        address signer;    // The person who signed the file
        bytes32 fileHash;  // The file's hash
        bytes signature;   // Digital signature
        uint256 timestamp; // Time of signing
    }

    // Mapping of file hashes to FileRecord
    mapping(bytes32 => FileRecord) public records;

    event FileSigned(address indexed signer, bytes32 fileHash, uint256 timestamp);

    // Function to store file signature
    function signFile(bytes32 fileHash, bytes memory signature) public {
        require(records[fileHash].signer == address(0), "File already signed");

        records[fileHash] = FileRecord({
            signer: msg.sender,
            fileHash: fileHash,
            signature: signature,
            timestamp: block.timestamp
        });

        emit FileSigned(msg.sender, fileHash, block.timestamp);
    }

    // Function to verify file signature
    function verifyFile(bytes32 fileHash) public view returns (address, bytes memory, uint256) {
        require(records[fileHash].signer != address(0), "File not signed");

        FileRecord memory record = records[fileHash];
        return (record.signer, record.signature, record.timestamp);
    }
}
