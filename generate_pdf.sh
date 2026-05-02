#!/bin/bash

# Generate PDF from the complete ebook
echo "Starting PDF generation for Idea2Creation ebook..."

# Create images directory if it doesn't exist
mkdir -p images

# Create placeholder images (in a real scenario, these would be actual images)
echo "Creating placeholder images for the ebook..."

# Create a simple cover image
cat > images/cover.svg << 'EOF'
<svg width="800" height="1200" xmlns="http://www.w3.org/2000/svg">
  <rect width="800" height="1200" fill="#667eea"/>
  <rect x="50" y="50" width="700" height="1100" fill="white" rx="20"/>
  
  <text x="400" y="300" font-family="Arial, sans-serif" font-size="48" font-weight="bold" text-anchor="middle" fill="#667eea">
    Idea2Creation
  </text>
  
  <text x="400" y="380" font-family="Arial, sans-serif" font-size="24" text-anchor="middle" fill="#666">
    The Complete Guide to AI Agentic Flows
  </text>
  
  <text x="400" y="420" font-family="Arial, sans-serif" font-size="24" text-anchor="middle" fill="#666">
    with OpenClaw
  </text>
  
  <text x="400" y="520" font-family="Arial, sans-serif" font-size="18" text-anchor="middle" fill="#764ba2">
    Generate Substantial Income from Idea to Creation
  </text>
  
  <text x="400" y="560" font-family="Arial, sans-serif" font-size="18" text-anchor="middle" fill="#764ba2">
    Using Our Special Formula
  </text>
  
  <text x="400" y="700" font-family="Arial, sans-serif" font-size="22" text-anchor="middle" fill="#333">
    By Poly Mintman
  </text>
  
  <rect x="300" y="800" width="200" height="60" fill="#667eea" rx="10"/>
  <text x="400" y="840" font-family="Arial, sans-serif" font-size="24" text-anchor="middle" fill="white">
    $99.00
  </text>
  
  <text x="400" y="1100" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#666">
    © 2026 Idea2Creation. All Rights Reserved.
  </text>
</svg>
EOF

# Convert SVG to PNG
if command -v convert &> /dev/null; then
    convert images/cover.svg images/cover.png
    echo "Created cover image: images/cover.png"
else
    echo "ImageMagick not found, using SVG directly"
fi

# Create diagram images
cat > images/architecture.svg << 'EOF'
<svg width="600" height="400" xmlns="http://www.w3.org/2000/svg">
  <style>
    .box { fill: #e3f2fd; stroke: #2196f3; stroke-width: 2; rx: 10; }
    .text { font-family: Arial, sans-serif; font-size: 14px; fill: #333; }
    .title { font-size: 16px; font-weight: bold; fill: #667eea; }
    .arrow { stroke: #666; stroke-width: 2; marker-end: url(#arrowhead); }
  </style>
  
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  
  <rect x="250" y="50" width="100" height="60" class="box"/>
  <text x="300" y="85" class="text title" text-anchor="middle">I2C</text>
  <text x="300" y="100" class="text" text-anchor="middle">Orchestrator</text>
  
  <rect x="50" y="150" width="100" height="60" class="box"/>
  <text x="100" y="185" class="text title" text-anchor="middle">Marketing</text>
  <text x="100" y="200" class="text" text-anchor="middle">Boss</text>
  
  <rect x="250" y="150" width="100" height="60" class="box"/>
  <text x="300" y="185" class="text title" text-anchor="middle">Operations</text>
  <text x="300" y="200" class="text" text-anchor="middle">Boss</text>
  
  <rect x="450" y="150" width="100" height="60" class="box"/>
  <text x="500" y="185" class="text title" text-anchor="middle">Customer</text>
  <text x="500" y="200" class="text" text-anchor="middle">Success Boss</text>
  
  <line x1="300" y1="110" x2="300" y2="150" class="arrow"/>
  <line x1="300" y1="110" x2="100" y2="150" class="arrow"/>
  <line x1="300" y1="110" x2="500" y2="150" class="arrow"/>
  
  <rect x="50" y="250" width="500" height="100" class="box" fill="#f3e5f5" stroke="#9c27b0"/>
  <text x="300" y="290" class="text title" text-anchor="middle">Development Team</text>
  <text x="300" y="310" class="text" text-anchor="middle">Frontend • Backend • DevOps • QA • Analytics</text>
  
  <line x1="100" y1="210" x2="100" y2="250" class="arrow"/>
  <line x1="300" y1="210" x2="300" y2="250" class="arrow"/>
  <line x1="500" y1="210" x2="500" y2="250" class="arrow"/>
  
  <text x="300" y="380" class="text" text-anchor="middle" font-size="12" fill="#666">
    9-Agent Architecture: Your Complete Digital Team
  </text>
</svg>
EOF

cat > images/workflow.svg << 'EOF'
<svg width="600" height="300" xmlns="http://www.w3.org/2000/svg">
  <style>
    .step { fill: #e8f5e9; stroke: #4caf50; stroke-width: 2; rx: 10; }
    .text { font-family: Arial, sans-serif; font-size: 14px; fill: #333; }
    .title { font-size: 16px; font-weight: bold; fill: #2e7d32; }
    .arrow { stroke: #666; stroke-width: 2; marker-end: url(#arrowhead); }
  </style>
  
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  
  <rect x="50" y="100" width="100" height="60" class="step"/>
  <text x="100" y="130" class="text title" text-anchor="middle">Idea</text>
  <text x="100" y="145" class="text" text-anchor="middle">Generation</text>
  
  <rect x="200" y="100" width="100" height="60" class="step"/>
  <text x="250" y="130" class="text title" text-anchor="middle">Product</text>
  <text x="250" y="145" class="text" text-anchor="middle">Creation</text>
  
  <rect x="350" y="100" width="100" height="60" class="step"/>
  <text x="400" y="130" class="text title" text-anchor="middle">Sales &</text>
  <text x="400" y="145" class="text" text-anchor="middle">Marketing</text>
  
  <rect x="500" y="100" width="100" height="60" class="step"/>
  <text x="550" y="130" class="text title" text-anchor="middle">Deployment</text>
  <text x="550" y="145" class="text" text-anchor="middle">& Scaling</text>
  
  <line x1="150" y1="130" x2="200" y2="130" class="arrow"/>
  <line x1="300" y1="130" x2="350" y2="130" class="arrow"/>
  <line x1="450" y1="130" x2="500" y2="130" class="arrow"/>
  
  <text x="300" y="50" class="text title" text-anchor="middle" font-size="18">
    Idea2Creation Workflow
  </text>
  
  <text x="300" y="220" class="text" text-anchor="middle" font-size="12" fill="#666">
    Automated Process from Idea to Income
  </text>
</svg>
EOF

# Convert SVG to PNG if ImageMagick is available
if command -v convert &> /dev/null; then
    convert images/architecture.svg images/architecture.png
    convert images/workflow.svg images/workflow.png
    echo "Created diagram images"
fi

# Create the complete HTML file with all content
echo "Creating complete HTML file..."

# Start with the template
cat ebook_template.html > ebook_with_images.html

# Insert the actual content after the introduction
# We'll use sed to insert content at the right place
# This is simplified - in production you'd use a more robust method

echo "Combining all content..."
cat ebook_all_content.md >> ebook_with_images.html

# Add closing tags
echo "</body></html>" >> ebook_with_images.html

echo "HTML file created: ebook_with_images.html"

# Check if pandoc is available
if ! command -v pandoc &> /dev/null; then
    echo "Error: pandoc is not installed. Installing..."
    apt-get update && apt-get install -y pandoc wkhtmltopdf
fi

# Generate PDF using pandoc
echo "Generating PDF..."
pandoc ebook_with_images.html \
  -o "Idea2Creation.pdf" \
  --pdf-engine=wkhtmltopdf \
  --table-of-contents \
  --toc-depth=3 \
  --number-sections \
  -V geometry:margin=2cm \
  -V fontsize=12pt \
  --metadata title="Idea2Creation: AI Super Agent Ebook" \
  --metadata author="Poly Mintman" \
  --metadata date="April 2026"

if [ $? -eq 0 ]; then
    echo "✅ PDF generated successfully: Idea2Creation.pdf"
    echo "📊 File size: $(du -h Idea2Creation.pdf | cut -f1)"
    echo "📄 Page count: $(pdfinfo Idea2Creation.pdf 2>/dev/null | grep Pages | awk '{print $2}' || echo 'Unknown')"
else
    echo "❌ PDF generation failed. Trying alternative method..."
    
    # Try alternative method
    if command -v wkhtmltopdf &> /dev/null; then
        wkhtmltopdf ebook_with_images.html Idea2Creation.pdf
        if [ $? -eq 0 ]; then
            echo "✅ PDF generated using wkhtmltopdf directly"
        else
            echo "❌ All PDF generation methods failed"
            echo "Please install: apt-get install pandoc wkhtmltopdf"
        fi
    fi
fi

echo "Process complete!"