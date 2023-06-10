import React from "react";
import {Link} from "react-router-dom";

import {Layout, Menu, theme} from "antd";
import {LogoutOutlined, UploadOutlined, VideoCameraOutlined} from "@ant-design/icons";

const Home: React.FC = () => {
  const {
    Content,
    Footer,
    Sider,
  } = Layout;

  const {
    token: {colorBgContainer},
  } = theme.useToken();

  return (
    <Layout style={{height: '100%'}}>
      <Sider>
        <div className="demo-logo-vertical"/>
        <Menu theme="dark" mode="inline" defaultSelectedKeys={['1']}>
          <Menu.Item key="logout" icon={<LogoutOutlined/>}>
            <Link to="/">Logout</Link>
          </Menu.Item>
          <Menu.Item key="upload" icon={<UploadOutlined/>}>
            <Link to="/upload">Upload</Link>
          </Menu.Item>
          <Menu.Item key="gallery" icon={<VideoCameraOutlined/>}>
            <Link to="/gallery">Gallery</Link>
          </Menu.Item>
        </Menu>
      </Sider>

      <Layout>
        <Content style={{height: '85%'}}>
          <div style={{padding: '20%', minHeight: 'calc(100vh - 120px)', background: colorBgContainer}}>
            <h1 style={{textAlign: 'center'}}>You are logged in</h1>
          </div>
        </Content>

        <Footer style={{textAlign: 'center', height: '20px', marginBottom: '15px'}}>
          MNIST Classification ©2023 Created by Jingbo Su
        </Footer>
      </Layout>
    </Layout>
  )
}

export default Home;
