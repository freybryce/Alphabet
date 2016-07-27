import facebook
token = 'EAAHQDNvMrgABAJfoObvmQl1QPaPMznPdTOyaY69eAVobHZCqjcEVueQEXoCyo7ZBHryzISRcyjcK5BPlQvZAKxsIVIpASttEmiZCJJtp5GsHVOS9S2W7zZAvyXNVWTtOdsvs4Hr5eipYPDiLiSXx0oQ8ZA15yFxiIY9BDZBfTRx5QZDZD'
graph = facebook.GraphAPI(access_token=token)
data = graph.request('/search?q=Clayton&type=user')
logging.info("Her is the data that Facebook is giving us: {data}".format(data=data))
