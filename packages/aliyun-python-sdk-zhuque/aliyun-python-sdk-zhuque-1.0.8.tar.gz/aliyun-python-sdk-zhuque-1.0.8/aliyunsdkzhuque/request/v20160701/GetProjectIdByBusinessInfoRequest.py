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
class GetProjectIdByBusinessInfoRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Zhuque', '2016-07-01', 'GetProjectIdByBusinessInfo')

	def get_CloudInstance(self):
		return self.get_query_params().get('CloudInstance')

	def set_CloudInstance(self,CloudInstance):
		self.add_query_param('CloudInstance',CloudInstance)

	def get_BusinessProjectId(self):
		return self.get_query_params().get('BusinessProjectId')

	def set_BusinessProjectId(self,BusinessProjectId):
		self.add_query_param('BusinessProjectId',BusinessProjectId)

	def get_ProjectType(self):
		return self.get_query_params().get('ProjectType')

	def set_ProjectType(self,ProjectType):
		self.add_query_param('ProjectType',ProjectType)

	def get_Locale(self):
		return self.get_query_params().get('Locale')

	def set_Locale(self,Locale):
		self.add_query_param('Locale',Locale)

	def get_Region(self):
		return self.get_query_params().get('Region')

	def set_Region(self,Region):
		self.add_query_param('Region',Region)

	def get_Azone(self):
		return self.get_query_params().get('Azone')

	def set_Azone(self,Azone):
		self.add_query_param('Azone',Azone)