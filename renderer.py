import os
from config import TEMP_DIR
import tempfile
import mapscript


class WmsRenderer:
    
    def __init__(self, map_repository):
        
        self.repo = map_repository
        
        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR)

    def render(self, mapname, query_string):
        
        map_data = self.repo.get_map_data(mapname)
        
        if not map_data:
            raise MapNotFoundError(f"Карта с именем '{mapname}' не найдена.")

        mapstyle_content, gjson_content = map_data
        
        json_filepath = os.path.join(TEMP_DIR, f"{mapname}.json")        
        
        try:
            with open(json_filepath, 'w', encoding='utf-8') as f:
                f.write(gjson_content)

            ows_request = mapscript.OWSRequest()
            ows_request.loadParamsFromURL(query_string)

            map_obj = mapscript.mapObj(map_string_content=mapstyle_content) 

            mapscript.msIO_installStdoutToBuffer()
            map_obj.OWSDispatch(ows_request)
            
            content_type = mapscript.msIO_stripStdoutBufferContentType()
            result_image = mapscript.msIO_getStdoutBufferBytes()
            
            return result_image, content_type

        finally:
            if os.path.exists(json_filepath):
                os.remove(json_filepath)
        
