fotos =  '[<div class="vwrQge" role="img" style="background-image:url(https://lh5.googleusercontent.com/p/AF1QipOIili9dRA_Ca4LeaNDmS2Z9PnSwGE00L2L-Z3l=w260-h175-n-k-no)"></div>, <div class="vwrQge" role="img" style="background-image:url(https://lh3.googleusercontent.com/p/AF1QipNV_ZV3SIc9ygvoyMJTSb4E8Zu1jKrsCDs3A6CC=w130-h87-n-k-no)"></div>, <div class="vwrQge" role="img" style="background-image:url(https://lh5.googleusercontent.com/p/AF1QipOUyJkdc79MzgJ5nfnX8-l-8T1IlBeNLtE79C_u=w130-h87-n-k-no)"></div>, <div class="vwrQge" role="img" style="background-image:url(https://lh5.googleusercontent.com/p/AF1QipOultz5bTd600MjRAG-5VtNqy7fbxqNgxyIKYw=w86-h87-n-k-no)"></div>, <div class="vwrQge" role="img" style="background-image:url(https://lh5.googleusercontent.com/p/AF1QipM_X4-uZcqPLKmaJczh3wCWNnKKVE77CfnqQWiw=w86-h87-n-k-no)"></div>, <div class="vwrQge" role="img" style="background-image:url(https://lh5.googleusercontent.com/p/AF1QipPo2Mzc-Y-v9otbMqQn1QlhqC_BASCq2EqKmZEx=w86-h87-n-k-no)"></div>]'
fotos = fotos.replace('<',"")
fotos = fotos.replace('>',"")

fotos = fotos.split(",")
print(fotos)
for url in fotos:
    pos1 = url.find('(')
    pos2 = url.find(")")
    link = url[pos1 + 1:pos2]
    print(link)



