import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "antd";
import { GlobalContext } from "../GlobalContext";

const DemoButton = () => {
  const navigate = useNavigate();
  const { setResult } = useContext(GlobalContext);
  return (
    <div>
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
