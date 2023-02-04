import { useContext, useEffect, useState } from "react";
import { Typography, Upload, Button, Row, Col } from "antd";
import { useNavigate } from "react-router-dom";
import { GlobalContext } from "./GlobalContext";

const { Title, Text } = Typography;

const Result = () => {
  const navigate = useNavigate();
  const { urls, result, width, height } = useContext(GlobalContext);

  return (
    <div className="my-0 mx-24">
      <Title className="text-center">결과</Title>

      <div className="flex justify-center text-center">
        <div className="m-2.5">
          <Title level={3}>원본</Title>
          <br />
          <img
            src={urls.origin}
            alt="background"
            width={width}
            className="border"
          />
        </div>
        <div className="m-2.5">
          <Title level={3}>번역본</Title>
          <br />
          <img
            src={
              result.data
                ? result.data
                : `https://via.placeholder.com/${width}x${height}`
            }
            alt="번역 결과"
            width={width}
            className="border"
          />
        </div>
      </div>

      <div className="p-0 my-0 mx-auto">
        <div className="flex justify-center">
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
