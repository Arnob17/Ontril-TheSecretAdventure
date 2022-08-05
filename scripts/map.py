from dataclasses import dataclass
from tkinter import dialog
import pygame, pytmx, pyscroll

from scripts.player import NPC
from scripts.storyTeller import StoryTell


@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    npcs: list[NPC]

class MapManager:

    def __init__(self, screen, player):

        self.maps = dict()

        self.screen = screen    

        self.player = player

        self.current_map = 'world'

        self.regester_map('world', portals=[
            Portal(from_world='world', origin_point="house_enter", target_world='house', teleport_point='spawn_house'),
            Portal(from_world='world', origin_point="enter_house_2", target_world='house2', teleport_point='spwan_house'),
            Portal(from_world='world', origin_point="lakeAqua_enter", target_world='lakeAqua', teleport_point='spawn_lake')
        ], npcs=[
            NPC('zen2', nb_points=4, dialog=['Me: Hey, My name is ontrie', 'Sio: Hello, I am Sio.', 'Me: I want to find my friends. Can you help me?', 'Sio: Sure!', 'Me: Do you know Mount Arnobest?', 'Sio: Nope.', 'Me: Lake Aqua?', 'Sio: Sorry..', 'Me: Then do you know? How can i find these locations?', 'Sio: Um, I dont know.. ask somebody else']),
            NPC('zen', nb_points=2, dialog=['Zen: Hello..?', 'Me: Hey, I am ontrie, I am new here', 'Zen: What you want to do here?', 'Me: I want to find my friends, can you help me..?', 'Zen: I am sorry, I cant. you can explore other places,', 'ask everyone for help.', 'Me: Mhm']),
            NPC('msd', nb_points=2, dialog=['Me: Hello there!', 'Msd: Hey!', 'Me: Can you help me?', 'Msd: Yea. But how?', 'Me: Do you know Mount Arnobest?', 'Msd: Nah.', 'Me: Castle Samir?', 'Msd: No. Sorry', 'Me: Can you say who can tell me these locations?', 'Msd: Yeah, Go to house number 11', 'on the west side of this city'])
        ])

        self.regester_map('house', portals=[
            Portal(from_world='house', origin_point="exit_house", target_world='world', teleport_point='spawn_world')
        ])

        self.regester_map('house2', portals=[
            Portal(from_world='house2', origin_point="exit_house", target_world='world', teleport_point='spawn_world_2'),
        ], npcs=[
            NPC('moon', nb_points=2, dialog=['Me: Hi..?', 'Moon: Mhm?', 'Me: So, can you help me?', 'Moon: Yeah how?', 'Me: Tell me where is Mount Arnobest', 'Moon: That cursed mount..', 'Moon: Well, I only know Lake Aqua.', 'Moon: W-why?', 'Moon: Dont ask questions. Go to the', 'east-north side of the town', 'Me: Then?', 'Moon: You will find a lake. The part of lake Aqua', 'Me: Yeah then?', 'Moon: In the lake you have to find the point of teleport.'])
        ])

        self.regester_map('lakeAqua', portals=[
            Portal(from_world='lakeAqua', origin_point="world_spawn_lake", target_world='world', teleport_point="back_world"),
            Portal(from_world='lakeAqua', origin_point="samirland_enter", target_world='samirland', teleport_point="samirland_enter")
        ], npcs=[
            NPC('zen', nb_points=2, dialog=['Nubah: Hello', 'Me: Hey, can i get some help?', 'Nubah: Sure', 'Nubah: I want to find my friends, can you help me..?', 'Nubah: okhey!', 'Me: Can you say me?', 'Me: Where can i find the princess of this lake?' 'Nubah: Keep going...']),
            NPC('zen2', nb_points=2, dialog=['Oxygen: Hey!', 'Me: Can you say me where can I find Aqua?', 'Oxygen: Keep going forward!', 'Me: Oh..']),
            NPC('msd', nb_points=2, dialog=['Radium: Hello', 'Me: Where can I find Aqua?', 'Radium: Go ahead!']),
            NPC('Aqua', nb_points=2, dialog=['Aqua: Oh finally you are here', 'Me: Hey, What happened to my friends?', 'Aqua: Calm down! I will help you for find the mystery', 'Me: But how?', 'Aqua: I think you know the famous', 'Aqua: The land of darkness' 'Me: Mhm', 'Aqua: Ya.', 'Aqua: Go to the land of darkness for find the mystery', 'Me: But you?', 'Aqua: Dont worry. I will be there']),
        ])

        self.regester_map('samirland', portals=[
            Portal(from_world='samirland', origin_point="samirland_exit", target_world='lakeAqua', teleport_point="world_spawn_lake")
        ], npcs=[
            NPC('msd', nb_points=2, dialog=['Samir: Hello', 'Me: Samir T_T. What happened?', 'Samir: Nothing, Its a dark mystery', 'Samir: That dark energy took everything from us..', 'Where is my other friends?', 'Go to the south west side of this land.']),
        ])

        self.teleport_player('player')

        self.teleport_npcs()

    def check_npc_collision(self, box):
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type ( sprite ) is NPC:
                box.execute(sprite.dialog)
                box.musicPlayer()

    def check_collision(self):

        for p in self.get_map().portals:
            
            if p.from_world == self.current_map:
                point = self.get_object(p.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = p
                    self.current_map = p.target_world
                    self.teleport_player(copy_portal.teleport_point)

        for x in self.get_group().sprites():

            if type(x) is NPC:
                if x.feet.colliderect(self.player.rect):
                    x.speed = 0
                else:
                    x.speed = 1

            if x.feet.collidelist(self.get_walls()) > -1:
                x.move_back()

        if self.current_map == 'lakeAqua':
            story = self.get_object('storytell')
            story_Rect = pygame.Rect(story.x, story.y, story.width, story.height)

            if self.player.feet.colliderect(story_Rect):
                story_teller = StoryTell()
                story_teller.execute_toggle(texts=['Hi :D', 'Hello :D'])  

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def regester_map(self, name, portals=[], npcs=[]):
        tmx_data = pytmx.util_pygame.load_pygame(f"{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

        map_layer.zoom = 2

        # player_position = tmx_data.get_object_by_name('player')

        # self.player = Player(player_position.x, player_position.y)

        walls = []

        for obj in tmx_data.objects:
            if obj.type == 'collision':
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        group.add(self.player)

        for npc in npcs:
            group.add(npc)


        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs)

    
    def get_map(self): return self.maps[self.current_map]

    def get_group(self): return self.get_map().group

    def get_walls(self): return self.get_map().walls

    def get_object(self, name): return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_npcs(self):

        for map1 in self.maps:
            map_data = self.maps[map1]
            npcs = map_data.npcs

            for npc in npcs:
                npc.load_points(map_data.tmx_data)

                npc.teleport_spawm()

    def draw(self):
        
        self.get_group().draw(self.screen)
        
        self.get_group().center(self.player.rect.center)

    def update(self):

        self.get_group().update()

        self.check_collision()


        for npc in self.get_map().npcs:
            npc.move()