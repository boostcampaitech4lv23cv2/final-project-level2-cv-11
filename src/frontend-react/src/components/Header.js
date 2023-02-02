import { useNavigate, Link } from "react-router-dom";
import { Typography } from "antd";
const { Title } = Typography;

const Header = () => {
  const navigate = useNavigate();
  return (
    <header>
      <div className="mx-24 mt-5 mb-2 border-b">
        <Title className="inline-block">
          <span
            className="cursor-pointer"
            onClick={() => {
              navigate("/");
            }}
          >
            Toonslator
          </span>
        </Title>
        <div className="inline-block ml-4">
          <Link to="/">Home</Link> &nbsp;
          <Link to="/demo">Demo</Link> &nbsp;
          <Link to="/result">Result</Link> &nbsp;
          <Link to="/edit">Edit</Link> &nbsp;
          <Link to="/loading">Loading</Link> &nbsp;
          <Link to="/dev">Dev</Link> &nbsp;
        </div>

        <div className="inline-block w-80 float-right"></div>
      </div>
    </header>
  );
};

export default Header;
