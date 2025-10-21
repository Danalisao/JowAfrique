/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: ['images.unsplash.com', 'via.placeholder.com', 'static.jow.fr'],
    unoptimized: false,
  },
  output: 'standalone',
  poweredByHeader: false,
  compress: true,
  generateEtags: true,
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY,
  },
}

module.exports = nextConfig
