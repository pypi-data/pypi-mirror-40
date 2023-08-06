from setuptools import setup, find_packages

setup(
    name="iotile_support_prod_pod1m_1",
    packages=find_packages(include=["iotile_support_prod_pod1m_1.*", "iotile_support_prod_pod1m_1"]),
    version="1.0.2",
    install_requires=['iotile_support_firm_env_1 >= 1.1.1, == 1.*', 'iotile_support_con_nrf52832_3 >= 3.1.12, == 3.*', 'iotile_support_firm_accelerometer_2 >= 2.3.5, == 2.*', u'sortedcontainers ~= 2.1', u'iotile-core >= 3.24.1', u'iotile-ext-cloud >= 0.6.0', u'iotile-sensorgraph >= 0.8.0'],
    entry_points={'iotile.app': ['tracker_app = iotile_support_prod_pod1m_1.tracker_app'], 'iotile.recipe_action': ['CalibratePOD1MStep = iotile_support_prod_pod1m_1.calibrate_pod1m_step:CalibratePOD1MStep', 'ResetPOD1MStep = iotile_support_prod_pod1m_1.reset_pod1m_step:ResetPOD1MStep']},
    author="Arch",
    author_email="info@arch-iot.com"
)