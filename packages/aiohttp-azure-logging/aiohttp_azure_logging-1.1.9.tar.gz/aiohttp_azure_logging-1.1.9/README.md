Logging Module for Azure Log Analytics


#### Install
- pip install aiohttp-azure-logging

#### Implement
```
from aiohttp_azure_logging import send_to_azure

app = web.application()
settings = {
	'workspace_id': '<YOUR WORKSPACE ID>',
	'workspace_secret' '<YOUR WORKSPACE PRIMARY OR SECONDARY KEY>'
}
send_to_azure(app, settings)
```

To send custom events:
```
async def my_view(request):
	await request.app['oms'].create_event(
		log_type='new_event_category'
		name='specific_event_name',
		request=request,
		event_data={
			'retry_attempts': 0,
			'success': True,
			'response_message': "Success",
			'nested_object': {
				'value_one': 'test'
			}
		})
```