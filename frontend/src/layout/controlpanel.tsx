import { useEffect, useState } from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

function ControlPanel() {
  const [models, setModels] = useState<any[]>([]);
  const [selectedModel, setSelectedModel] = useState<any | null>(null);

// ... existing code ...
useEffect(() => {
  const backendUrl = import.meta.env.VITE_BACKEND_URL;

  const fetchData = async () => {
    try {
      const response = await fetch(`${backendUrl}/llm/models`);
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const responseData = await response.json();
      setModels(responseData.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  fetchData(); // Remove 'await' here

}, []);
const handleSelectChange = (selectedModelId: string) => {
  const selectedModel = models.find(model => model.id === selectedModelId);
  console.log(selectedModel);
  setSelectedModel(selectedModel);
};
  return (
    <div className="w-full h-full pt-[10px] px-4 space-y-4">
      {models.length > 0 ? (
        <Select onValueChange={handleSelectChange}>
          <SelectTrigger className="w-full">
            <SelectValue placeholder="Select Model" />
          </SelectTrigger>
          <SelectContent className="bg-white">
            {models.map((model) => (
            <SelectItem  key={model.id}  value={model.id}>
              {model.name}
            </SelectItem>
          ))}
          </SelectContent>
        </Select>
      ) : (
        <p>loading </p>
      )}
      <div className="w-full h-[120px] border border-[#71717A]/30 rounded-md overflow-y-auto p-2 text-[12px]">
      <code>
      {selectedModel?
        selectedModel.description:"The model is described as follows:"
      }
      </code>
      </div>
    </div>
  );
}

export default ControlPanel;
