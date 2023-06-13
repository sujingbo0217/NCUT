import io

import torch
import torch.nn.functional as F
import torchvision.transforms as transforms

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet

from PIL import Image
from mnist.mnist.mlp import MLP
from utils.response import APIResponse
from utils.request import get_request, get_image
# middleware import

from .models import Images
from .serializers import UserSerializer, ImageSerializer, ImageInfoSerializer
# models import

# Create your views here.
class UserViewSet(ViewSet):
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="User register",
        manual_parameters=[
            openapi.Parameter(
                'username',
                openapi.IN_QUERY,
                description="Username",
                required=True,
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'password',
                openapi.IN_QUERY,
                description="Password",
                required=True,
                type=openapi.TYPE_STRING,
            ),
        ],
        security=[], tags=['User'], operation_summary='Create a new user',
        responses={status.HTTP_200_OK: '200', status.HTTP_404_NOT_FOUND: '404'})
    def user_register(self, request: Request):
        result = get_request(request, openapi.IN_QUERY)
        username = result.get('username')
        password = result.get('password')
        queryset = Images.objects.all()
        is_existed = queryset.filter(username=username).exists()
        if is_existed:
            return APIResponse(error='User exists', status=status.HTTP_400_BAD_REQUEST)

        reg_info = dict({
            'username': username,
            'password': password,
        })

        serializer = self.serializer_class(data=reg_info)
        if serializer.is_valid(raise_exception=True):
            register = serializer.create(reg_info)
            register.save()
            if register:
                return APIResponse(user=username, status=status.HTTP_201_CREATED)

        return APIResponse(serializer.data, error='User register failed', status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="User login",
        manual_parameters=[
            openapi.Parameter(
                'username',
                openapi.IN_QUERY,
                description="Username",
                required=True,
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'password',
                openapi.IN_QUERY,
                description="Password",
                required=True,
                type=openapi.TYPE_STRING,
            ),
        ],
        security=[], tags=['User'], operation_summary='User login',
        responses={status.HTTP_200_OK: '200', status.HTTP_404_NOT_FOUND: '404'})
    def user_login(self, request: Request):
        result = get_request(request, openapi.IN_QUERY)
        username = result.get('username')
        password = result.get('password')
        queryset = Images.objects.all()
        user = queryset.filter(username=username)

        is_existed = user.exists()
        if not is_existed:
            return APIResponse(error='User not exists', status=status.HTTP_404_NOT_FOUND)

        user = user.first()
        if user.password != password:
            return APIResponse(error='Wrong password', status=status.HTTP_400_BAD_REQUEST)

        user_id = user.id
        request.session['user_id'] = user_id
        return APIResponse(user=username, status=status.HTTP_200_OK)


class ImageViewsSet(ViewSet):
    serializer_class = ImageSerializer

    # ************************** GET *************************** #

    @swagger_auto_schema(
        operation_description="Get an image download url by ID",
        manual_parameters=[
        ],
        security=[], tags=['MNIST'], operation_summary='Get all images',
        responses={status.HTTP_200_OK: '200', status.HTTP_404_NOT_FOUND: '404'})
    def display(self, request: Request):
        queryset = Images.objects.all()
        serializer = ImageInfoSerializer(instance=queryset, many=True)
        return APIResponse(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get an image download url by ID",
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_QUERY,
                description="image ID",
                required=True,
                type=openapi.TYPE_INTEGER
            ),
        ],
        security=[], tags=['MNIST'], operation_summary='Get download url',
        responses={status.HTTP_200_OK: '200', status.HTTP_404_NOT_FOUND: '404'})
    def download(self, request: Request):
        _id = get_request(request, openapi.IN_QUERY).get('id')
        # image = Images.objects.get(id=_id)
        queryset = Images.objects.all()
        image = queryset.filter(id=_id)
        serializer = self.serializer_class(image)
        return APIResponse(data=serializer, img_url=image.image.url)

    # ************************** POST *************************** #

    @swagger_auto_schema(
        operation_description="Upload an image",
        manual_parameters=[
            openapi.Parameter(
                'label',
                openapi.IN_FORM,
                description="Image label",
                required=True,
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'image',
                openapi.IN_FORM,
                description="Image to be predicted",
                required=True,
                type=openapi.TYPE_FILE,
            ),
        ],
        security=[], tags=['MNIST'], operation_summary='Upload an image',
        responses={status.HTTP_200_OK: '200', status.HTTP_404_NOT_FOUND: '404'})
    def upload(self, request: Request):
        result = get_request(request, openapi.IN_BODY)

        # created = datetime.now()
        label = result.get('label')  # True label
        name, image = get_image(request, 'image')
        pred, prob = self.predict(image)

        image_data = dict({
            'image': image,
            'name': name,
            'label': label,
            'pred': str(pred),
            'prob': str(prob)[:5],
            'result': (int(pred) == int(label)),
        })

        try:
            serializer = self.serializer_class(data=image_data)
            if serializer.is_valid(raise_exception=True):
                image_result = serializer.create(image_data)
                if image_result:
                    return APIResponse(serializer.data, status=status.HTTP_201_CREATED)
                return APIResponse(status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
        except Exception as e:
            print(e)

    # ************************** DELETE *************************** #

    @swagger_auto_schema(
        operation_description="Delete an image by ID",
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_QUERY,
                description="image ID",
                required=True,
                type=openapi.TYPE_INTEGER
            ),
        ],
        security=[], tags=['MNIST'], operation_summary='Delete an image',
        responses={status.HTTP_200_OK: '200', status.HTTP_404_NOT_FOUND: '404'})
    def delete(self, request: Request):
        _id = get_request(request, openapi.IN_QUERY).get('id')
        image = Images.objects.get(id=_id)
        if image is not None:
            image.delete()
            return APIResponse(status=status.HTTP_200_OK)
        return APIResponse(status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def predict(image):
        # Preprocess the input image
        input_image = Image.open(io.BytesIO(image.read()))
        transform = transforms.Compose([
            transforms.Resize((28, 28)),
            transforms.Grayscale(),
            transforms.ToTensor(),
        ])
        input_image = transform(input_image).unsqueeze(0)

        # Predict the image use mlp
        net = MLP(28 * 28, 10)
        net.load_state_dict(torch.load('mnist/mnist/mnist.pt', map_location=torch.device('cpu')))
        net.eval()

        with torch.no_grad():
            pred, _ = net(input_image)
            prob = F.softmax(pred, dim=-1)

            for i, p in enumerate(prob[0]):
                print(f'p({i}) = {p}')

            _pred = pred.argmax(dim=1, keepdim=True).item()
            _prob = torch.max(prob).item()

        return _pred, _prob
