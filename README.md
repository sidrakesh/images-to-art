# Images to Art

This project focuses on image processing techniques for converting images to pieces of art.

## Quilling

[Quilling](https://en.wikipedia.org/wiki/Quilling) or paper filigree is an art form that involves the use of strips of paper that are rolled, shaped, and glued together to create decorative designs.

This method simulates the art of quilling on images. It uses [Delaunay Triangulation](http://www.degeneratestate.org/posts/2017/May/24/images-to-triangles/) to create segments of the image, and matplotlib for drawing the various shapes.

How to run (got good results at `number_of_points = 800`):

```
python convert-to-quilling.py -n <number of points> <input file path> <output file path>
```

Examples:

![bird](https://user-images.githubusercontent.com/6567881/147434368-cbf8083b-e639-4a0f-b2fc-95e9d195fe47.jpg)
![dog2](https://user-images.githubusercontent.com/6567881/147434413-f2648164-40de-4d8c-a5ae-383a73360e80.jpg)
![fox](https://user-images.githubusercontent.com/6567881/147434441-5204c831-8a03-45f8-988c-c1d18a63c2d2.jpg)
![monkey](https://user-images.githubusercontent.com/6567881/147434447-33598934-facc-4ecf-9047-082099673b66.jpg)
![octopus](https://user-images.githubusercontent.com/6567881/147434449-e97271a3-bbfc-4d31-8345-5af86f2cb9a7.jpg)
![seal](https://user-images.githubusercontent.com/6567881/147434450-c47e2106-2c18-45a0-92b8-e0714cbe5797.jpg)

## Line intersection

This method uses Adaptive filtering for reducing noise, and generates max entropy points on the image. Then, lines are drawn through nearby points on the image (they shouldnt be too close though, because then there will be too many unnecessary lines).

How to run (got good results at `number_of_points = 800`):

```
python convert-to-lines.py -n <number of points> <input file path> <output file path>
```

Examples:

![g1](https://user-images.githubusercontent.com/6567881/147846654-548369e1-fc94-48fd-89fe-06104212f3a7.jpg)
![bird](https://user-images.githubusercontent.com/6567881/147846652-1d6b195f-e5c1-415a-bc38-bbadef1ec166.jpg)
![b2](https://user-images.githubusercontent.com/6567881/147846651-3b767845-0ec4-45b6-859d-6763d0ced3b0.jpg)
![cat2](https://user-images.githubusercontent.com/6567881/147846653-8f4d013c-df6c-46b0-bca8-39d0b12ce969.jpg)
![stag](https://user-images.githubusercontent.com/6567881/147846657-cff908cf-0157-43ae-a3cf-6742253d36a1.jpg)
![rg1](https://user-images.githubusercontent.com/6567881/147846656-65d38bc3-0430-4888-895b-b1ba47723c75.jpg)
