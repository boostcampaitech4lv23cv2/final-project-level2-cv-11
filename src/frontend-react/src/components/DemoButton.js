import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Button, message } from "antd";
import { GlobalContext } from "../GlobalContext";

const DemoButton = () => {
  const navigate = useNavigate();
  const { files, setResult } = useContext(GlobalContext);
  return (
    <div>
      <Button
        onClick={() => {
          if (!files.background || !files.typical || !files.untypical) {
            message.error("배경, 대사, 효과음 레이어를 모두 업로드 해주세요.");
            return;
          }
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
