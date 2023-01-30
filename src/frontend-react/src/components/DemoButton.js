import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "antd";
import { FileContext } from "../FileContext";

const DemoButton = () => {
  const navigate = useNavigate();
  const { setResult } = useContext(FileContext);
  return (
    <div style={{ textAlign: "center" }}>
      <Button
        onClick={() => {
          setResult({ data: null, boxes: null });
          navigate("/loading");
        }}
      >
        번역하기
      </Button>
    </div>
  );
};

export default DemoButton;
