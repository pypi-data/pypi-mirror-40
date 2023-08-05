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
class AddProjectRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Zhuque', '2016-07-01', 'AddProject')

	def get_ProjectName(self):
		return self.get_query_params().get('ProjectName')

	def set_ProjectName(self,ProjectName):
		self.add_query_param('ProjectName',ProjectName)

	def get_Creator(self):
		return self.get_query_params().get('Creator')

	def set_Creator(self,Creator):
		self.add_query_param('Creator',Creator)

	def get_CloudInstance(self):
		return self.get_query_params().get('CloudInstance')

	def set_CloudInstance(self,CloudInstance):
		self.add_query_param('CloudInstance',CloudInstance)

	def get_Manager(self):
		return self.get_query_params().get('Manager')

	def set_Manager(self,Manager):
		self.add_query_param('Manager',Manager)

	def get_DeliveryDay(self):
		return self.get_query_params().get('DeliveryDay')

	def set_DeliveryDay(self,DeliveryDay):
		self.add_query_param('DeliveryDay',DeliveryDay)

	def get_Description(self):
		return self.get_query_params().get('Description')

	def set_Description(self,Description):
		self.add_query_param('Description',Description)

	def get_Locale(self):
		return self.get_query_params().get('Locale')

	def set_Locale(self,Locale):
		self.add_query_param('Locale',Locale)

	def get_Plan_pattern(self):
		return self.get_query_params().get('Plan_pattern')

	def set_Plan_pattern(self,Plan_pattern):
		self.add_query_param('Plan_pattern',Plan_pattern)

	def get_BusinessProjectId(self):
		return self.get_query_params().get('BusinessProjectId')

	def set_BusinessProjectId(self,BusinessProjectId):
		self.add_query_param('BusinessProjectId',BusinessProjectId)

	def get_ProjectOrigin(self):
		return self.get_query_params().get('ProjectOrigin')

	def set_ProjectOrigin(self,ProjectOrigin):
		self.add_query_param('ProjectOrigin',ProjectOrigin)

	def get_ProjectType(self):
		return self.get_query_params().get('ProjectType')

	def set_ProjectType(self,ProjectType):
		self.add_query_param('ProjectType',ProjectType)

	def get_Region(self):
		return self.get_query_params().get('Region')

	def set_Region(self,Region):
		self.add_query_param('Region',Region)

	def get_Azone(self):
		return self.get_query_params().get('Azone')

	def set_Azone(self,Azone):
		self.add_query_param('Azone',Azone)