import { useContext } from "react";
import { Typography } from "antd";
import { useNavigate } from "react-router-dom";
import { GlobalContext } from "./GlobalContext";

const { Title } = Typography;

const Result = () => {
  const navigate = useNavigate();
  const { urls, result, width, height } = useContext(GlobalContext);

  return (
    <div className="my-0 mx-24 mb-24">
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
          <button
            class="bg-blue-500 hover:bg-blue-700 text-white text-3xl font-bold py-4 px-6 rounded m-3"
            onClick={() => {
              navigate("/edit");
            }}
          >
            편집
          </button>
          <button
            class="bg-blue-500 hover:bg-blue-700 text-white text-3xl font-bold py-4 px-6 rounded m-3 inline-flex"
            onClick={() => {
              const a = document.createElement("a");
              a.href = result.data;
              a.download = "result.png";
              a.click();
            }}
          >
            <svg
              class="fill-current w-8 h-8 mr-2"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
            >
              <path d="M13 8V2H7v6H2l8 8 8-8h-5zM0 18h20v2H0v-2z" />
            </svg>
            <span>다운로드</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Result;
