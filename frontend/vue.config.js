var path = require('path');

module.exports = {
  chainWebpack: config => {
    config.resolve.alias.set('@views', path.resolve('src/views'));
    config.resolve.alias.set('@components', path.resolve('src/components'));
    config.resolve.alias.set('@hooks', path.resolve('src/hooks'));
    config.resolve.alias.set('@api', path.resolve('src/api'));
    config.resolve.alias.set('@store', path.resolve('src/store'));
    config.resolve.alias.set('@style', path.resolve('src/assets/css'));
  }
};
