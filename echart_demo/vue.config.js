module.exports = {
  outputDir: "../dist/root",
  productionSourceMap: true,
  devServer: {
    proxy: {
      // 设置代理
      "/api": {
        target: "http://127.0.0.1:80",
        ws: true, // 代理websocket
        changeOrigin: true // 将主机标头的原点更改为目标URL
      }
    }
  }
};
