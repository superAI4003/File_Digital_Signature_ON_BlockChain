 import { useState } from "react";
import { AiOutlineSend } from "react-icons/ai";
import ReactLoading from 'react-loading';

function ContentPanel() {
  const [isGenerating, setIsGenerating] = useState(false);
  return (
    <div className="w-full h-full bg-[#ffffff] rounded-t-lg shadow-lg relative">
      <div className="  py-2 pl-6 pr-2 absolute bottom-3 left-1/2 transform -translate-x-1/2 mb-4 w-8/12 flex items-center border rounded-full shadow-sm ">
        <input
          type="text"
          className="w-full  border-none  focus:border-none focus:outline-none hover:border-none px-2 text-[18px]"
          placeholder="Type your message..."
        />
        <button
        onClick={()=>setIsGenerating(!isGenerating)}
        className="w-[50px] h-[50px] bg-black justify-center items-center flex rounded-full hover:bg-black/80">
          {!isGenerating?
            <AiOutlineSend size={20} className="text-white" />:    <ReactLoading type="bars" color="#ffffff" height={25} width={25} />
}
        </button>
      </div>
    </div>
  );
}

export default ContentPanel;
