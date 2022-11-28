import os

from aiohttp import web

from app import BASE_DIR
from app.base.application import View
from app.store.ws.ws_accessor import WSContext


class IndexView(View):
    async def get(self):
        with open(os.path.join(BASE_DIR, 'client', 'index.html'), 'r') as f:
            file = f.read()

        return web.Response(
            body=file,
            headers={
                'Content-Type': 'text/html',
            }
        )

class IndexViewIcon(View):
    async def get(self):
        # with open(os.path.join(BASE_DIR, 'client', 'static', 'favicon.svg'), 'rb') as f:
        with open(os.path.join(BASE_DIR, 'client', 'static', '9025026_smiley_light_icon.png'), 'rb') as f:
            file = f.read()
        
        return web.Response(
            body=file,
            content_type='image/x-icon'
        )


class WSConnectView(View):
    async def get(self):
        async with WSContext(
                accessor=self.store.wsAccessor,
                request=self.request,
                close_callback=self.store.geoManager.on_user_disconnect,
        ) as connection_id:
            await self.store.geoManager.handle(connection_id)
        return
