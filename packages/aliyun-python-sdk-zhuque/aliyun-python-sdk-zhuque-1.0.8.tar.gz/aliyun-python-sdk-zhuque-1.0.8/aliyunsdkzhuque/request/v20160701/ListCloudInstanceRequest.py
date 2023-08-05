# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
class ListCloudInstanceRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Zhuque', '2016-07-01', 'ListCloudInstance')

	def get_DisplayName(self):
		return self.get_query_params().get('DisplayName')

	def set_DisplayName(self,DisplayName):
		self.add_query_param('DisplayName',DisplayName)

	def get_CloudType(self):
		return self.get_query_params().get('CloudType')

	def set_CloudType(self,CloudType):
		self.add_query_param('CloudType',CloudType)

	def get_CustomerId(self):
		return self.get_query_params().get('CustomerId')

	def set_CustomerId(self,CustomerId):
		self.add_query_param('CustomerId',CustomerId)

	def get_Locale(self):
		return self.get_query_params().get('Locale')

	def set_Locale(self,Locale):
		self.add_query_param('Locale',Locale)