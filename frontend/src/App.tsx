import React, { useState } from "react";
import axios from "axios";

enum LoadingState {
  None = "none",
  SignLoading = "signLoading",
  VerifyLoading = "verifyLoading",
}

function App() {
  const [loading, setLoading] = useState(LoadingState.None);
  const [signmessage, setSignMessage] = useState("Try to Digital Signature");
  const [verifymessage, setVerifyMessage] = useState(
    "Try to Verify Digital Signature"
  );
  const [status, setStatus] = useState("Thanks for visiting!");
  const handleSignFileChange = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (file) {
      setLoading(LoadingState.SignLoading);
      setSignMessage("Loading...");
      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await axios.post(
          `${import.meta.env.VITE_BACKEND_URL}/upload-file/`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        if(response.data.result){
          setSignMessage("Done successfully!");
          setStatus(`Transaction Hash: ${response.data.tx_hash}`);
          }
        else{
          setSignMessage('Failed Signing!');
          setStatus(`Failed: ${response.data.tx_hash}`);
        }
       
      } catch (error) {
        setStatus("Error uploading file");
      } finally {
        setLoading(LoadingState.None);
      }
    } 
  };
  const handleVerifyFileChange = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (file) {
      setLoading(LoadingState.VerifyLoading);
      setVerifyMessage("Loading...");
      const formData = new FormData();
      formData.append("file", file);

      try {
        // Update the endpoint to verify the signature
        const response = await axios.post(
          `${import.meta.env.VITE_BACKEND_URL}/verify-signature/`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );

        // Check if the verification was successful
        if (response.data.verified) {
          setVerifyMessage("Signature Verified")
          setStatus(
            `Signature Verified! Signer: ${response.data.signer}`
          );
        } else {
          setVerifyMessage(" Verified failed")
          setStatus("Signature verification failed");
        }
      } catch (error) {
        setStatus("Error verifying file");
      } finally {
        setLoading(LoadingState.None);
      }
    }
  };

  return (
    <div
      className="flex justify-center items-center h-screen flex-col bg-sky-800/10"
  
    > 
      <div className="px-10 pt-16 pb-10  bg-gray-400/20 rounded-lg drop-shadow-xl">
        <h1 className="text-5xl leading-none font-extrabold text-gray-900 tracking-tight mb-4">
          Getting Start with Digital Signature.
        </h1>
        <p className="text-2xl tracking-tight mb-10 text-gray-500">
          The best security on blockchain is achieved through decentralized consensus mechanisms.
        </p>
        <div className="space-x-4">
          <label className="p-4 bg-gray-800 hover:bg-gray-600 text-white hover:cursor-pointer">
            {signmessage}
            <input
              type="file"
              style={{ display: "none" }}
              onChange={handleSignFileChange}
            />
          </label>
          <label className="p-4 bg-gray-800 hover:bg-gray-600 text-white hover:cursor-pointer">
            {verifymessage}
            <input
              type="file"
              style={{ display: "none" }}
              onChange={handleVerifyFileChange}
            />
          </label>
        </div>
        <div className="w-full  mt-9 bg-gray-800 shadow-lg rounded-xl">
          <p className="flex-auto text-white text-lg font-medium px-4 py-2">
            <span className="text-red-600">Status</span> {status}
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
