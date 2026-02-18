# Creating Photo Frames

## Format Requirements

Photo frames for the photobooth must be:
- **Format**: PNG
- **Transparency**: Yes (alpha channel required)
- **Recommended Size**: 1920x1080 pixels (Full HD)
- **Color Mode**: RGBA

## Frame Structure

A frame consists of:
1. **Border/Decorations**: Opaque elements (frames, text, graphics)
2. **Photo Area**: Transparent center where the captured photo will be visible
3. **Overlays**: Optional decorative elements on top of the photo

## Example Frame Layout

```
┌─────────────────────────────────────┐
│  ◄──── Decorative Border ────►     │
│  ┌───────────────────────────┐     │
│  │                           │     │
│  │   Transparent Photo Area  │     │
│  │   (Alpha = 0)             │     │
│  │                           │     │
│  └───────────────────────────┘     │
│                                     │
│  Text or Logo Here                 │
│  (Opaque, Alpha = 255)             │
└─────────────────────────────────────┘
```

## Design Tips

### 1. Leave Enough Space
- Ensure the transparent area is large enough for the subject
- Recommended: At least 60-70% of the image should be transparent
- Keep decorations to the edges

### 2. Contrast
- Use colors that contrast well with various backgrounds
- Consider adding a subtle shadow or stroke to text
- Test with different lighting conditions

### 3. Branding
- Add your logo or event name
- Include date or event information
- Use consistent brand colors

### 4. Themes
Create frames for different occasions:
- **Wedding**: Romantic elements, hearts, flowers
- **Birthday**: Balloons, confetti, celebration
- **Corporate**: Logo, company colors, professional
- **Seasonal**: Holiday themes, seasonal decorations

## Creating a Frame in Photoshop

1. **Create new document**
   - Size: 1920x1080 pixels
   - Color Mode: RGB Color
   - Background: Transparent

2. **Design the frame**
   - Add border elements on separate layers
   - Keep center area transparent
   - Add text/graphics as needed

3. **Export**
   - File > Export > Export As
   - Format: PNG
   - Transparency: Checked
   - Save to: `assets/frames/`

## Creating a Frame in GIMP

1. **Create new image**
   - Width: 1920, Height: 1080
   - Advanced Options > Fill with: Transparency

2. **Design the frame**
   - Use layers for different elements
   - Keep center transparent using eraser tool
   - Add decorations on edges

3. **Export**
   - File > Export As
   - Select file type: PNG
   - Save in: `assets/frames/`
   - Export options: Save background color: No

## Simple Frame with Python (Pillow)

```python
from PIL import Image, ImageDraw, ImageFont

# Create new image with transparency
width, height = 1920, 1080
img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw border
border_width = 50
border_color = (255, 255, 255, 200)  # White with some transparency

# Top border
draw.rectangle([0, 0, width, border_width], fill=border_color)
# Bottom border
draw.rectangle([0, height-border_width, width, height], fill=border_color)
# Left border
draw.rectangle([0, 0, border_width, height], fill=border_color)
# Right border
draw.rectangle([width-border_width, 0, width, height], fill=border_color)

# Add text
try:
    font = ImageFont.truetype("arial.ttf", 60)
except:
    font = ImageFont.load_default()

text = "Photobooth 2024"
text_bbox = draw.textbbox((0, 0), text, font=font)
text_width = text_bbox[2] - text_bbox[0]
text_x = (width - text_width) // 2
text_y = height - border_width + 10

draw.text((text_x, text_y), text, fill=(0, 0, 0, 255), font=font)

# Save
img.save('assets/frames/simple_frame.png')
```

## Testing Your Frame

1. Save the frame in `assets/frames/`
2. Launch the application: `python main.py`
3. The frame will appear on the home screen
4. Select it and test with the camera
5. Adjust as needed

## Frame Collection Examples

### Minimal Frame
```
Simple border with text at bottom
Transparent center: 80%
```

### Decorative Frame
```
Ornate borders with corner decorations
Text and graphics
Transparent center: 65%
```

### Polaroid Style
```
White border with wider bottom
Space for "photo date" or caption
Transparent center: 70%
```

### Event Frame
```
Event logo in corner
Date and location
Theme-specific decorations
Transparent center: 70%
```

## Resources

### Free Frame Templates
- Create your own using the methods above
- Modify example frames
- Commission a designer for custom frames

### Design Tools
- **Photoshop**: Professional, paid
- **GIMP**: Free, open-source
- **Canva**: Online, templates available
- **Inkscape**: Vector graphics, free

### Inspiration
- Pinterest: "Photo booth frames"
- Instagram: #photobooth
- Event-specific themes

## Tips for Best Results

1. **Test with real photos**: Try the frame with actual captures
2. **Consider orientation**: Design works for both portrait subjects
3. **File size**: Keep under 5MB for better performance
4. **Multiple versions**: Create several for variety
5. **Seasonal updates**: Refresh frames for different seasons/events
