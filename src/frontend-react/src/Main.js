import { Typography } from "antd";
import { useNavigate } from "react-router-dom";

const { Title } = Typography;

const Members = () => {
  return (
    <div>
      <h1 className="text-3xl font-bold">팀 소개</h1>
      <Title level={5}>저희 팀을 소개합니다</Title>
      <div className="flex justify-center">
        <div className="mx-4">
          <img src="https://via.placeholder.com/150" alt="team member" />
          <h2>류건</h2>
          <p>역할</p>
        </div>
        <div className="mx-4">
          <img src="https://via.placeholder.com/150" alt="team member" />
          <h2>심건희</h2>
          <p>역할</p>
        </div>
        <div className="mx-4">
          <img src="https://via.placeholder.com/150" alt="team member" />
          <h2>윤태준</h2>
          <p>역할</p>
        </div>
        <div className="mx-4">
          <img src="https://via.placeholder.com/150" alt="team member" />
          <h2>이강희</h2>
          <p>역할</p>
        </div>
        <div className="mx-4">
          <img src="https://via.placeholder.com/150" alt="team member" />
          <h2>이예라</h2>
          <p>역할</p>
        </div>
      </div>
    </div>
  );
};

const Main = () => {
  const navigate = useNavigate();
  return (
    <>
      <div className="mx-24 text-center">
        <div className="text-left h-[60vh] align-middle pt-40 border-b">
          <h1 className="text-8xl font-medium">Toonslator</h1>
          <h1 className="text-3xl font-bold">
            생동감 있는 웹툰 자동 번역 서비스
          </h1>

          <button
            class="bg-blue-500 hover:bg-blue-700 text-white text-3xl font-bold py-4 px-6 rounded m-6"
            onClick={() => {
              navigate("/demo");
            }}
          >
            Start
          </button>
        </div>

        <div className="pb-24 my-8 border-b">
          <h1 className="text-3xl font-bold">발표 영상</h1>
          <div className="flex justify-center mt-8">
            <iframe
              width="800"
              height="400"
              src="https://www.youtube.com/embed/Jy2VKCZ2d3k"
              title="네이버 Boostcamp AI Tech 최종프로젝트 - 웹툰 번역(Toonslator)"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
              allowfullscreen
            ></iframe>
          </div>
        </div>

        <div className="h-10" />

        <Members />
        <div className="h-10" />
      </div>
    </>
  );
};

export default Main;
