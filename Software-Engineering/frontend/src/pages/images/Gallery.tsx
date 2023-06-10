import React from "react";
import {Link} from "react-router-dom";

import {Col, Layout, Menu, Row, theme, Image} from "antd";
import {LogoutOutlined, UploadOutlined, VideoCameraOutlined} from "@ant-design/icons";

const Gallery: React.FC = () => {
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
          <div style={{paddingLeft: '20%', paddingRight: '20%', paddingTop: '10%', minHeight: 'calc(100vh - 120px)', background: colorBgContainer}}>
            <Image.PreviewGroup
              preview={{
                onChange: (current, prev) => console.log(`current index: ${current}, prev index: ${prev}`),
              }}
            >
              <Row gutter={[16, 16]}>
                {[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,].map(() => (
                  <Col span={4}>
                    <div>Description</div>
                    <Image src="https://gw.alipayobjects.com/zos/antfincdn/aPkFc8Sj7n/method-draw-image.svg"/>
                  </Col>
                ))}
              </Row>
            </Image.PreviewGroup>
          </div>
        </Content>

        <Footer style={{textAlign: 'center', height: '20px', marginBottom: '15px'}}>
          MNIST Classification ©2023 Created by Jingbo Su
        </Footer>
      </Layout>
    </Layout>
  )
}

export default Gallery;
