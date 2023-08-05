# -*- coding: utf-8 -*-
"""
Eureka Client.

Eureka is a service discovery and registration service
built by Netflix and used in the Spring Cloud stack.
"""
import atexit
import enum
import time
import requests

from http import HTTPStatus
from threading import Thread
from typing import Optional, Dict, Any

from .utils import get_host_ip
from .log import logger


class EurekaException(Exception):
    def __init__(self, status: HTTPStatus, *args, **kwargs):
        self._status = status
        super().__init__(*args, **kwargs)

    @property
    def status(self) -> HTTPStatus:
        return self._status


class StatusType(enum.Enum):
    """
    服务状态值枚举类型
    """
    UP = 'UP'
    DOWN = 'DOWN'
    STARTING = 'STARTING'
    OUT_OF_SERVICE = 'OUT_OF_SERVICE'
    UNKNOWN = 'UNKNOWN'


class EurekaClient(object):

    def __init__(self,
                 app_name: Optional[str] = None,
                 port: Optional[int] = None,
                 ip_addr: Optional[str] = None,
                 *,
                 hostname: Optional[str] = None,
                 eureka_url: str = 'http://localhost:8761',
                 instance_id: Optional[str] = None,
                 health_check_url: Optional[str] = None,
                 status_page_url: Optional[str] = None):
        """
        基础的注册，注销和刷新功能，暂不支持https

        :param app_name: 应用名称
        :param port: 注册的服务端口
        :param ip_addr: 当前主机IP
        :param hostname: 当前主机域名，若未设置则取当前主机IP
        :param eureka_url: Eureka注册中心地址
        :param instance_id: 服务实例ID=`host_ip : app_name : port`
        :param health_check_url: 心跳健康检查路径，默认为`/`
        :param status_page_url: 状态页跳转路径，默认为flasggerAPI文档路径`/apidocs/`
        """
        self._eureka_url = eureka_url.rstrip('/') + '/eureka'
        self._app_name = app_name
        self._port = port
        self._secure_port = 443
        # 若不设置，则取当前主机IP
        self._ip_addr = ip_addr or get_host_ip()
        self._hostname = hostname or self._ip_addr
        self._health_check_url = health_check_url

        self._instance_id = instance_id
        if status_page_url is None:
            status_page_url = 'http://{}:{}/apidocs/'.format(self._ip_addr,
                                                             port)
            logger.debug('Status page not provided, rewriting to %s',
                         status_page_url)
        self._status_page_url = status_page_url
        # 心跳间隔
        self._lease_duration = 60
        self._lease_renewal_interval = 15

    def register(self, metadata: Optional[Dict[str, Any]] = None):
        """

        :return:
        """
        payload = {
            'instance': {
                'instanceId': self.instance_id,
                'leaseInfo': {
                    'durationInSecs': self._lease_duration,
                    'renewalIntervalInSecs': self._lease_renewal_interval,
                },
                'port': {
                    '$': self._port,
                    '@enabled': self._port is not None,
                },
                'hostName': self._hostname,
                'app': self._app_name,
                'ipAddr': self._ip_addr,
                'vipAddress': self._app_name,
                'dataCenterInfo': {
                    '@class': 'com.netflix.appinfo.MyDataCenterInfo',
                    'name': 'MyOwn',
                },
            }
        }
        if self._health_check_url is not None:
            payload['instance']['healthCheckUrl'] = self._health_check_url
        if self._status_page_url is not None:
            payload['instance']['statusPageUrl'] = self._status_page_url
        if metadata:
            payload['instance']['metadata'] = metadata
        url = '/apps/{}'.format(self._app_name)
        logger.debug('Registering %s', self._app_name)
        return self._do_req(url, method='POST', data=payload)

    def renew(self):
        """Renews the application's lease with eureka to avoid
        eradicating stale/decommissioned applications."""
        url = '/apps/{}/{}'.format(self._app_name, self.instance_id)
        return self._do_req(url, method='PUT')

    def deregister(self):
        """Deregister with the remote server, if you forget to do
        this the gateway will be giving out 500s when it tries to
        route to your application."""
        url = '/apps/{}/{}'.format(self._app_name, self.instance_id)
        return self._do_req(url, method='DELETE')

    def set_status_override(self, status: StatusType):
        """Sets the status override, note: this should generally only
        be used to pull services out of commission - not really used
        to manually be setting the status to UP falsely."""
        url = '/apps/{}/{}/status?value={}'.format(self._app_name,
                                                   self.instance_id,
                                                   status.value)
        return self._do_req(url, method='PUT')

    def remove_status_override(self):
        """Removes the status override."""
        url = '/apps/{}/{}/status'.format(self._app_name,
                                          self.instance_id)
        return self._do_req(url, method='DELETE')

    def update_meta(self, key: str, value: Any):
        url = '/apps/{}/{}/metadata?{}={}'.format(self._app_name,
                                                  self.instance_id,
                                                  key, value)
        return self._do_req(url, method='PUT')

    def get_apps(self) -> Dict[str, Any]:
        """Gets a payload of the apps known to the
        eureka server."""
        url = '/apps'
        return self._do_req(url)

    def get_app(self, app_name: Optional[str] = None) -> Dict[str, Any]:
        app_name = app_name or self._app_name
        url = '/apps/{}'.format(app_name)
        return self._do_req(url)

    def get_app_instance(self, app_name: Optional[str] = None,
                         instance_id: Optional[str] = None):
        """Get a specific instance, narrowed by app name."""
        app_name = app_name or self._app_name
        instance_id = instance_id or self.instance_id
        url = '/apps/{}/{}'.format(app_name, instance_id)
        return self._do_req(url)

    def get_instance(self, instance_id: Optional[str] = None):
        """Get a specific instance, without needing to care about
        the app name."""
        instance_id = instance_id or self.instance_id
        url = '/instances/{}'.format(instance_id)
        return self._do_req(url)

    def get_by_vip(self, vip_address: Optional[str] = None):
        """Query for all instances under a particular vip address"""
        vip_address = vip_address or self._app_name
        url = '/vips/{}'.format(vip_address)
        return self._do_req(url)

    def get_by_svip(self, svip_address: Optional[str] = None):
        """Query for all instances under a particular secure vip address"""
        svip_address = svip_address or self._app_name
        url = '/vips/{}'.format(svip_address)
        return self._do_req(url)

    def _do_req(self, path: str, *, method: str = 'GET',
                data: Optional[Dict] = None):
        """
        Performs a request against the instance eureka server.
        :param path: URL Path, the hostname is prepended automatically
        :param method: request method (put/post/patch/get/etc)
        :param data: Optional data to be sent with the request, must
                     already be encoded appropriately.
        :return: optional[dict[str, any]]
        """
        url = self._eureka_url + path
        logger.debug('Performing %s on %s with payload: %s', method, path,
                     data)
        resp = requests.request(method, url, json=data or {})
        if 400 <= resp.status_code < 600:
            raise EurekaException(HTTPStatus(resp.status_code), resp.text)
        logger.debug('Result status: %s', resp.status_code)
        return resp.text

    def _generate_instance_id(self) -> str:
        """Generates a unique instance id"""
        instance_id = '{}:{}:{}'.format(
            self._ip_addr, self._app_name, self._port)
        logger.debug('Generated new instance id: %s for app: %s', instance_id,
                     self._app_name)
        return instance_id

    @property
    def app_name(self):
        """The app_name the eureka client is targeting

        :return:
        """
        return self._app_name

    @property
    def instance_id(self) -> str:
        """The instance_id the eureka client is targeting"""
        if self._instance_id is None:
            self._instance_id = self._generate_instance_id()
        # noinspection PyTypeChecker
        return self._instance_id

    def start(self):
        """
        Start registration process
        :return:
        """
        logger.info('Starting eureka registration')
        # 注册
        self.register()
        # 心跳线程
        heartbeat_task = Thread(target=self._heartbeat)
        heartbeat_task.daemon = True
        heartbeat_task.start()
        # 注销
        atexit.register(self.deregister)
        logger.info('Register app %s to eureka successfully', self.app_name)

    def _heartbeat(self):
        """

        :return:
        """
        while True:
            try:
                time.sleep(self._lease_duration)
                self.renew()
            except Exception as e:
                logger.error('Eureka connection Exception, {}'.format(e))
