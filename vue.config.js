module.exports = {
    configureWebpack: {

    },
    pluginOptions: {
        electronBuilder: {
            builderOptions: {
                extraResources: {
                    from: 'pydist',
                    to: 'pydist'
                }
            }
        }
    }
}