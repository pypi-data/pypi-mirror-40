# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import sys
import json
import os
import requests
import six


def get_exp_info():
    """Returns the task info: {"type": "worker|master|ps", "index": int}."""
    info = os.getenv('AUTOCNN_EXP_INFO', None)
    try:
        return json.loads(info) if info else None
    except (ValueError, TypeError):
        print('Could get job info, '
              'please make sure this is running inside a autocnn job.')
        return None


def get_api(version='v1'):
    api = os.getenv('SEETAAS_HELPER_API', None)
    if not api:
        print('Could get api info, '
              'please make sure this is running inside a autocnn job.')
        return None
    return '{}'.format(api)

def get_autocnn_parameter():
    autocnn_parameter = os.getenv('AUTOCNN_PARAMETER', None)
    try:
        return json.loads(autocnn_parameter) if autocnn_parameter else None
    except (ValueError, TypeError):
        print('Could get autocnn parameter, '
              'please make sure this is running inside a autocnn job.')
        return None
    

def send_metrics(**metrics):
    """Sends metrics to seetaas helper api.

    Example:
        send_metric(precision=0.9, accuracy=0.89, loss=0.01)
    """
    exp_info = get_exp_info()
    exp_uuid = exp_info.get('exp_uuid', None)
    parameter_info = get_autocnn_parameter()
    #dataset_id = parameter.get('DEDUCTION_DATASET_ID', None)
    #dir_list_id = parameter.get('DIR_LIST_ID', None)
    label_dataset_id = os.getenv('DEDUCTION_DATASET_ID', None)
    origin_dataset_id = os.getenv('ORIGIN_DATASET_ID', None)
    dir_list_id = os.getenv('DIR_LIST_ID', None)
    api = get_api()
    if not all([exp_uuid, label_dataset_id, origin_dataset_id, dir_list_id, api]):
        print('Environment information not found, '
              'please make sure this is running inside a autocnn job.')
        return

    try:
        formatted_metrics = {k: v for k, v in six.iteritems(metrics)}
    except (ValueError, TypeError):
        print('Could not send metrics {}'.format(metrics))
        return
    try:
        requests.post('{}/api/helper/metrics/deduction/{}'.format(api, exp_uuid),
                      data={'label_dataset_id': label_dataset_id, 'origin_dataset_id': origin_dataset_id, 'dir_list_id': dir_list_id,'values': json.dumps(formatted_metrics)})
    except requests.RequestException as e:
        print('Could not reach autocnn api {}'.format(e))
