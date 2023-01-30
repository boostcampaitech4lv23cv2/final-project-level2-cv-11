import { useContext, useEffect, useState } from "react";
import { Typography, Upload, Button, Row, Col } from "antd";
import { useNavigate } from "react-router-dom";
import { UploadOutlined } from "@ant-design/icons";
import styled from "styled-components";
import { FileContext } from "./FileContext";

const { Title, Text } = Typography;

const Div = styled.div`
  display: flex;
  justify-content: space-around;
  text-align: center;
`;

const Result = () => {
  const navigate = useNavigate();
  const { files, result } = useContext(FileContext);
  const [before, setBefore] = useState(null);

  useEffect(() => {
    const file = files["background"];
    if (file) {
      setBefore(URL.createObjectURL(file));
    }
  }, [files]);

  return (
    <div style={{ margin: "0 100px" }}>
      <Title>결과물 확인</Title>

      <Div>
        <div>
          <Title level={3}>원본</Title>
          <br />
          <img
            src={before}
            alt="background"
            width="300px"
            style={{
              border: "1px solid black",
            }}
          />
        </div>
        <div>
          <Title level={3}>번역본</Title>
          <br />
          <img
            src={result.data}
            alt="background"
            width="300px"
            style={{
              border: "1px solid black",
            }}
          />
        </div>
      </Div>

      <div style={{ height: "200px" }} />
      <div style={{ padding: "0 auto", margin: "0 auto" }}>
        <div
          style={{
            display: "flex",
            justifyContent: "center",
          }}
        >
          <Button
            onClick={() => {
              navigate("/edit");
            }}
          >
            편집
          </Button>
          <Button>공유(미구현)</Button>
          <Button
            onClick={() => {
              const a = document.createElement("a");
              a.href = result.data;
              a.download = "result.png";
              a.click();
            }}
          >
            저장
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Result;
