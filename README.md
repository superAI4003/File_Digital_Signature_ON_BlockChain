# File Digital Signature on Blockchain

## Overview

This project implements a digital signature system on the blockchain, allowing users to sign and verify files securely. The system is composed of three main components: a smart contract written in Solidity, a frontend application built with React, and a backend service using FastAPI.




## Getting Started

To get started with the project, follow these steps:

1. **Clone the Repository**: Clone the project repository to your local machine.
https://github.com/superAI4003/File_Digital_Signature_ON_BlockChain
2. **Install Dependencies**: Install the necessary dependencies for the frontend, backend, and smart contract.
    - **Smart Contract**: Navigate to the `blocksign` directory and run `npm install` to install the necessary dependencies for the smart contract.
    - **Frontend**: Navigate to the `frontend` directory and run `npm install` to install the necessary dependencies for the frontend application.
    - **Backend**: Navigate to the `backend` directory and run `pip install -r requirements.txt` to install the necessary dependencies for the backend service.
3. **Configure Environment Variables**: Set up the required environment variables for connecting to the Ethereum network and other configurations.
    - **Smart Contract**: Create a .env File:
    ```bash
    INFURA_URL=https://polygon-amoy.g.alchemy.com/v2/2aYZd16tO0F_sSP0lCGR65qfdhc77cFA
    PRIVATE_KEY = 0x4f18aaec864fe9bdac7c5029f8c5964525ae058f33ec8811df938860a7965b37
    ADDRESS = 0xe369703dFcA8496dEAb62f8F6f86fa885d684423
    CONTRACT_ADDRESS=0xbF779f722D9677D3E1017F9d3DEe536775699561
    ```

    - **Frontend**:Create a .env File:
    ```bash
     VITE_BACKEND_URL = http://127.0.0.1:8080
    ```

    - **Backend**:Create a .env File:
    ```bash
    INFURA_URL=https://polygon-amoy.g.alchemy.com/v2/2aYZd16tO0F_sSP0lCGR65qfdhc77cFA
    PRIVATE_KEY = 0x4f18aaec864fe9bdac7c5029f8c5964525ae058f33ec8811df938860a7965b37
    ADDRESS = 0xe369703dFcA8496dEAb62f8F6f86fa885d684423
    ```

4. **Deploy the Smart Contract**: Use Hardhat to deploy the smart contract to your desired Ethereum network.
   ```bash
   npx hardhat compile
   ```
    ```bash
    npx hardhat ignition deploy ./ignition/modules/Lock.js --network goerli
    ```
    Afer deploy smart contract, you can get contract address.

    How to create wallet address.
    ```bash
    cd blocksign
    ```

    ```bash
    node createWallet.js
    ```
    You can get address and private key.
    
5. **Run the Backend**: Start the FastAPI backend server.
   ```bash
   uvicorn main:app --reload --port 8080
   ```
6. **Run the Frontend**: Start the React frontend application.
   ```bash
   npm run dev
   ```

