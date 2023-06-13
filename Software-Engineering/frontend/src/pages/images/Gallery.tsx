import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";

import {Menu, Layout, theme, Card, Button, Modal, message} from "antd";
import {LogoutOutlined, UploadOutlined, VideoCameraOutlined, DownloadOutlined} from "@ant-design/icons";

import {imageType, responseType, imageInfoType} from "../../types/images";
import {deleteImage, displayImage} from "../../apis/images";
import Empty from "./Empty";
import "./Gallery.css";

const Gallery: React.FC = () => {
  const {
    Content,
    Footer,
    Sider,
  } = Layout;

  const {
    token: {colorBgContainer},
  } = theme.useToken();

  const [selectedImage, setSelectedImage] = useState<imageType | null>(null);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [images, setImages] = useState<imageType[]>([]);
  const [emptyPage, setEmptyPage] = useState(false);

  const fetchImages = async (): Promise<void> => {
    try {
      const response = await displayImage() as responseType;
      const record = response.content.record;

      if (response.result_code === 200) {
        if (record.length === 0) {
          setEmptyPage(true);
          return ;
        }
        const newImageArray: imageType[] = record.map((img: imageInfoType) => {
          const result: string = img.result ? 'Correct' : 'Wrong';
          const description = `${img.label}/${img.pred} | p = ${img.prob}`;
          return {
            id: img.id,
            url: `${import.meta.env.VITE_APP_BASE_API}${img.url}`,
            result: result,
            description: description,
          };
        });
        setImages(newImageArray);
      } else {
        message.error(response.error);
      }
    } catch (e) {
      console.log(e);
    }
  }

  useEffect(() => {
    fetchImages().then().catch(err => {
      console.log(err);
    });
  }, []);

  const handleDeleteImage = async (id: number) => {
    setImages(prevImages => prevImages.filter(image => image.id !== id));
    for (let i = 0; i < images.length; i++) {
      if (images[i].id === id) {
        const response = await deleteImage(String(id)) as responseType;
        const result_code = response.result_code;
        if (result_code === 200) {
          message.success('Image deleted').then();
        } else {
          message.error('Image deleted failed').then();
        }
        break;
      }
    }
  };

  const handleImageClick = (image: imageType) => {
    setSelectedImage(image);
    setIsModalVisible(true);
  };

  const handleModalClose = () => {
    setSelectedImage(null);
    setIsModalVisible(false);
  };

  if (emptyPage) {
    return (<Empty />);
  }

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
          <div
            style={{
              paddingLeft: '5%',
              paddingRight: '5%',
              paddingTop: '5%',
              minHeight: 'calc(100vh - 120px)',
              background: colorBgContainer
            }}
          >
            <div className="gallery">
              {images.map(image => (
                <Card
                  key={image.id}
                  hoverable
                  style={{ width: 150, margin: 10 }}
                  cover={<img src={image.url} alt={'error'} className="resized-image"/>}
                  onClick={() => handleImageClick(image)}
                  actions={[
                    <Button onClick={() => handleDeleteImage(image.id)} danger>
                      Delete
                    </Button>,
                    <Button>
                      <a href={image.url} download>
                        <DownloadOutlined/>
                      </a>
                    </Button>,
                  ]}
                >
                  <Card.Meta title={image.result} description={image.description} />
                </Card>
              ))}
            </div>
            <Modal
              visible={isModalVisible}
              onCancel={handleModalClose}
              footer={null}
            >
              {selectedImage && (
                <img src={selectedImage.url} alt={'error'} style={{ width: '100%' }} />
              )}
            </Modal>
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
