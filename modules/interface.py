import obspython as obs

class initialize():
    def __init__(self):
        self.source = obs.obs_frontend_get_current_scene()
        self.currentscene = obs.obs_scene_from_source(self.source)
        
        self.createGroup()
        self.group = obs.obs_scene_get_group(self.currentscene, "SpicetifyOBS")
        self.createImage()
        
        obs.obs_source_release(self.source)

    def positionItem(self, source, x, y):
        pos = obs.vec2()
        obs.obs_sceneitem_get_pos(source, pos)
        pos.x += x
        pos.y += y
        
        obs.obs_sceneitem_set_pos(source, pos)  

    def groupItem(self, item, position=[]):
        source = obs.obs_sceneitem_group_add_item(self.group, item)
        
    def createGroup(self):
        if not obs.obs_scene_get_group(self.currentscene, "SpicetifyOBS"):
            group = obs.obs_scene_add_group2(self.currentscene, "SpicetifyOBS", True)
    
    def createImage(self):
        settings = obs.obs_data_create()
        source = obs.obs_source_create_private("browser_source", "Album Art", settings)
        item = obs.obs_scene_add(self.currentscene, source)
        self.groupItem(item, [100, 100])
        
 # Classes like update etc