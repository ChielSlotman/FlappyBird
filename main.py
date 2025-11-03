import asyncio
import random

import pygame

def draw_floor():
	screen.blit(floor_surface,(floor_x_pos,900))
	screen.blit(floor_surface,(floor_x_pos + 576,900))

def create_pipe():
	global next_pipe_with_head
	random_pipe_pos = random.choice(pipe_height)
	if next_pipe_with_head:
		img = pipe_with_head
	else:
		img = pipe_without_head
	next_pipe_with_head = not next_pipe_with_head
	bottom_pipe = (img, img.get_rect(midtop = (700,random_pipe_pos)))
	top_pipe = (img, img.get_rect(midbottom = (700,random_pipe_pos - 300)))
	return bottom_pipe, top_pipe

def move_pipes(pipes):
	for pipe_img, pipe_rect in pipes:
		pipe_rect.centerx -= 5
	return pipes

def draw_pipes(pipes):
	for pipe_img, pipe_rect in pipes:
		if pipe_rect.bottom >= 1024:
			screen.blit(pipe_img, pipe_rect)
		else:
			flip_pipe = pygame.transform.flip(pipe_img, False, True)
			screen.blit(flip_pipe, pipe_rect)
def remove_pipes(pipes):
	for pipe_img, pipe_rect in pipes:
		if pipe_rect.centerx == -600:
			pipes.remove((pipe_img, pipe_rect))
	return pipes
def check_collision(pipes):
	for pipe_img, pipe_rect in pipes:
		if bird_rect.colliderect(pipe_rect):
			death_sound.play()
			return False

	if bird_rect.top <= -100 or bird_rect.bottom >= 900:
		return False

	return True

def rotate_bird(bird):
	new_bird = pygame.transform.rotozoom(bird,-bird_movement * 3,1)
	return new_bird

def bird_animation():
	new_bird = bird_frames[bird_index]
	new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
	return new_bird,new_bird_rect

def score_display(game_state):
	if game_state == 'main_game':
		score_surface = game_font.render(str(int(score)),True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,100))
		screen.blit(score_surface,score_rect)
	if game_state == 'game_over':
		score_surface = game_font.render(f'Score: {int(score)}' ,True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,100))
		screen.blit(score_surface,score_rect)

		high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(255,255,255))
		high_score_rect = high_score_surface.get_rect(center = (288,850))
		screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score

pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',40)
small_font = pygame.font.Font('04B_19.ttf',24)
badge_font = pygame.font.Font('04B_19.ttf',20)

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = False
score = 0
high_score = 0
show_notification_message = False
notification_seen = False
notification_icon = pygame.Surface((48,48), pygame.SRCALPHA)
pygame.draw.circle(notification_icon,(255,215,0),(24,24),24)
pygame.draw.circle(notification_icon,(90,70,0),(24,24),24,3)
icon_text = small_font.render('!',True,(40,40,40))
icon_text_rect = icon_text.get_rect(center = (24,23))
notification_icon.blit(icon_text,icon_text_rect)
notification_icon_rect = notification_icon.get_rect(center = (288,200))

notification_badge = pygame.Surface((26,26),pygame.SRCALPHA)
pygame.draw.circle(notification_badge,(220,30,20),(13,13),13)
pygame.draw.circle(notification_badge,(255,240,240),(13,13),13,2)
badge_text = badge_font.render('+1',True,(255,255,255))
badge_text_rect = badge_text.get_rect(center = (13,12))
notification_badge.blit(badge_text,badge_text_rect)
notification_badge_rect = notification_badge.get_rect(midbottom = (notification_icon_rect.right, notification_icon_rect.top + 6))

notification_hint = small_font.render('Klik op het icoon voor een bericht van Chiel!',True,(255,255,0))
notification_hint_rect = notification_hint.get_rect(center = (notification_icon_rect.centerx, notification_icon_rect.bottom + 32))

notification_lines = [
	'He Teon, hier Chiel met een bericht.',
	'Jij speelt elk spel met vol gezicht.',
	'Slim en scherp, altijd paraat,',
	'en in elk spel de grote maat.',
	'Maar nu in Flappy Teon, mijn vriend,',
	'wil ik zien of jij die vijftien wint.',
	'Dus flap die vleugels, blijf in de lucht,',
	'en laat zien dat winnen jou ook hier lukt.'
]
notification_header = small_font.render('Bericht van Chiel',True,(255,215,0))
notification_text_surfaces = [small_font.render(line,True,(230,230,230)) for line in notification_lines]
max_line_width = max(notification_header.get_width(), max(surface.get_width() for surface in notification_text_surfaces))
panel_padding = 28
panel_width = max_line_width + panel_padding * 2
panel_height = panel_padding * 2 + notification_header.get_height() + 12
for surface in notification_text_surfaces:
	panel_height += surface.get_height() + 6
panel_height -= 6
notification_panel = pygame.Surface((panel_width,panel_height),pygame.SRCALPHA)
panel_rect = notification_panel.get_rect()
pygame.draw.rect(notification_panel,(0,0,0,210),panel_rect,border_radius = 18)
pygame.draw.rect(notification_panel,(255,215,0,235),panel_rect,2,border_radius = 18)
notification_panel.blit(notification_header,(panel_padding, panel_padding))
y_offset = panel_padding + notification_header.get_height() + 12
for surface in notification_text_surfaces:
	notification_panel.blit(surface,(panel_padding,y_offset))
	y_offset += surface.get_height() + 6
notification_panel_rect = notification_panel.get_rect(center = (288,420))

pipe_without_head = pygame.transform.scale2x(pygame.image.load('assets/pipe_without_head.png'))
pipe_with_head = pygame.transform.scale2x(pygame.image.load('assets/pipe_with_head.png'))
next_pipe_with_head = False

bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100,512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

# bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
# bird_surface = pygame.transform.scale2x(bird_surface)
# bird_rect = bird_surface.get_rect(center = (100,512))

pipe_list = []
scored_pipes = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [400,600,800]

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288,512))
success_surface = pygame.transform.scale2x(pygame.image.load('assets/success.png').convert_alpha())

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

def trigger_flap():
	bird_jump_strength = 7.5
	global bird_movement
	bird_movement = 0
	bird_movement -= bird_jump_strength
	flap_sound.play()

def reset_game_state():
	global game_active, pipe_list, scored_pipes, next_pipe_with_head
	global show_notification_message, bird_rect, bird_movement, score
	game_active = True
	pipe_list.clear()
	scored_pipes.clear()
	next_pipe_with_head = False
	show_notification_message = False
	bird_rect.center = (100,512)
	bird_movement = 0
	score = 0

def handle_primary_press(pos):
	global show_notification_message, notification_seen
	if game_active:
		trigger_flap()
		return
	if notification_icon_rect.collidepoint(pos):
		if not notification_seen:
			show_notification_message = True
			notification_seen = True
		else:
			show_notification_message = not show_notification_message
	else:
		reset_game_state()

async def main():
	global bird_movement, game_active, pipe_list, scored_pipes, next_pipe_with_head
	global show_notification_message, notification_seen, bird_rect, score, floor_x_pos, bird_index, bird_surface, high_score
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				handle_primary_press(event.pos)
			if event.type == pygame.FINGERDOWN:
				finger_pos = (int(event.x * screen.get_width()), int(event.y * screen.get_height()))
				handle_primary_press(finger_pos)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and game_active:
					trigger_flap()
				if event.key == pygame.K_SPACE and game_active == False:
					reset_game_state()

			if event.type == SPAWNPIPE:
				pipe_list.extend(create_pipe())

			if event.type == BIRDFLAP:
				if bird_index < 2:
					bird_index += 1
				else:
					bird_index = 0

				bird_surface,bird_rect = bird_animation()

		screen.blit(bg_surface,(0,0))

		if game_active:
			# Bird
			bird_movement += gravity
			rotated_bird = rotate_bird(bird_surface)
			bird_rect.centery += bird_movement
			screen.blit(rotated_bird,bird_rect)
			game_active = check_collision(pipe_list)

			# Pipes
			pipe_list = move_pipes(pipe_list)
			pipe_list = remove_pipes(pipe_list)
			draw_pipes(pipe_list)

			# Score: add point only when bird passes a pipe
			for pipe_img, pipe_rect in pipe_list:
				if pipe_rect.centerx < bird_rect.left and (pipe_img, pipe_rect) not in scored_pipes and pipe_rect.bottom >= 1024:
					score += 1
					scored_pipes.append((pipe_img, pipe_rect))
					score_sound.play()
			score_display('main_game')
		else:
			if score >= 15:
				screen.blit(success_surface,game_over_rect)
			else:
				screen.blit(game_over_surface,game_over_rect)
			high_score = update_score(score,high_score)
			score_display('game_over')
			if not notification_seen:
				screen.blit(notification_hint,notification_hint_rect)
				screen.blit(notification_badge,notification_badge_rect)
				screen.blit(notification_icon,notification_icon_rect)
			elif show_notification_message:
				screen.blit(notification_panel,notification_panel_rect)


		# Floor
		floor_x_pos -= 1
		draw_floor()
		if floor_x_pos <= -576:
			floor_x_pos = 0
		

		pygame.display.update()
		clock.tick(120)
		await asyncio.sleep(0)

asyncio.run(main())
