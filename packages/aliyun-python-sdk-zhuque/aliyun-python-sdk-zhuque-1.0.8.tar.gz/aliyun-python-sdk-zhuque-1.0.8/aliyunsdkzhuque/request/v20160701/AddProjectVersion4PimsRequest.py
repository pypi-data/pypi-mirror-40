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
class AddProjectVersion4PimsRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Zhuque', '2016-07-01', 'AddProjectVersion4Pims')

	def get_Creator(self):
		return self.get_query_params().get('Creator')

	def set_Creator(self,Creator):
		self.add_query_param('Creator',Creator)

	def get_Description(self):
		return self.get_query_params().get('Description')

	def set_Description(self,Description):
		self.add_query_param('Description',Description)

	def get_BusinessVersionId(self):
		return self.get_query_params().get('BusinessVersionId')

	def set_BusinessVersionId(self,BusinessVersionId):
		self.add_query_param('BusinessVersionId',BusinessVersionId)

	def get_Locale(self):
		return self.get_query_params().get('Locale')

	def set_Locale(self,Locale):
		self.add_query_param('Locale',Locale)

	def get_ProjectId(self):
		return self.get_query_params().get('ProjectId')

	def set_ProjectId(self,ProjectId):
		self.add_query_param('ProjectId',ProjectId)

	def get_VersionName(self):
		return self.get_query_params().get('VersionName')

	def set_VersionName(self,VersionName):
		self.add_query_param('VersionName',VersionName)