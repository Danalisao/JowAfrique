const fs = require('fs')
const path = require('path')

// Créer les icônes PWA si elles n'existent pas
const createIcon = (size, filename) => {
  const svg = `<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="${size}" height="${size}" rx="${size/8}" fill="#0f172a"/>
<svg x="${size/4}" y="${size/4}" width="${size/2}" height="${size/2}" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="2">
<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
</svg>
</svg>`
  
  const publicDir = path.join(__dirname, '..', 'public')
  if (!fs.existsSync(publicDir)) {
    fs.mkdirSync(publicDir, { recursive: true })
  }
  
  fs.writeFileSync(path.join(publicDir, filename), svg)
  console.log(`✅ Created ${filename}`)
}

// Créer les icônes
createIcon(192, 'icon-192x192.png')
createIcon(512, 'icon-512x512.png')

console.log('🎉 PWA setup completed!')
