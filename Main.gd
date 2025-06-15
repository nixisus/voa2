extends Control

func _ready():
	$TopBar.color = Color.DIM_GRAY
	$RetroViewportContainer.material = null  # No tint on Viewport
	$BottomUI.modulate = Color("3b4cca")      # Blue-ish bottom
	$BottomUI/RichTextLabel_Log.text = "[b]Welcome to Vanity of Angels[/b]\nChoose your path below."
