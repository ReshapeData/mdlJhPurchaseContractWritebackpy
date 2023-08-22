#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mdlJhPurchaseContractWritebackpy import *
import pytest


@pytest.mark.parametrize('token,output',
                         [("C0426D23-1927-4314-8736-A74B2EF7A039", True)])

def test_purchaseContract_update(token,output):

    assert purchaseContract_update(token=token) == output