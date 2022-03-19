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

This method works well on images which have a clear background and high contrast of the image with the background.

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
![hb](https://user-images.githubusercontent.com/6567881/147846669-6f0a621b-0ec0-4310-b32e-13af53aed825.jpg)


## Constellations

This method uses Adaptive filtering for reducing noise, and generates max entropy points on the image. Then, stars are created on each entropy point, and the star size is determined based on the entropy value.

This method works well on images which have a clear background and high contrast of the image with the background.

How to run (got good results at `number_of_points = 800-1600`):

```
python convert-to-stars.py -n <number of points> -b <background color> <input file path> <output file path>
```

Examples:

![bird4](https://user-images.githubusercontent.com/6567881/148687978-c0141684-d86c-43e7-9654-a1054a96f439.jpeg)
![bird6](https://user-images.githubusercontent.com/6567881/148687996-d02c962a-3a55-4ee4-83ff-f801d88bce9a.jpg)
![dog2](https://user-images.githubusercontent.com/6567881/148687997-be566c15-8c0d-49eb-8b08-3289298de122.jpg)
![g11](https://user-images.githubusercontent.com/6567881/148688001-0294aae6-bbbe-4a2a-8a99-721550cdaa4a.jpg)
![peacock2](https://user-images.githubusercontent.com/6567881/148688003-808dc585-bd5c-472c-a7eb-dfd6573f52df.jpg)
![stag2](https://user-images.githubusercontent.com/6567881/148688004-73f10b68-c195-4213-b090-2fee391bb3ba.jpg)

## Short lines

This method uses Adaptive filtering for reducing noise, and generates max entropy points on the image. Then, nearest point groups are created by joining points whose distance is less than the average distance between all nearest neighbors. Each connected component is given a random color form a pre-determined set of colors.

This method works well on images which have a clear background and high contrast of the image with the background.

How to run (got good results at `number_of_points = 1600-3200`):

```
python convert-to-short-lines.py -n <number of points> <input file path> <output file path>
```

Examples:

![sol](https://user-images.githubusercontent.com/6567881/159117491-369d52cc-de4d-4cb6-a2ee-660fa47940f3.jpg)
![et](https://user-images.githubusercontent.com/6567881/159117484-18c3848f-4b07-4ecd-8a08-53117fd3015c.jpg)
![ig](https://user-images.githubusercontent.com/6567881/159117486-7bd489b2-0b3b-48e8-946e-56f6101e4132.jpg)
![qm](https://user-images.githubusercontent.com/6567881/159117488-d67a2a12-ee89-45d8-be40-95c9f1c8ec3e.jpg)
![soh](https://user-images.githubusercontent.com/6567881/159117490-ef11e963-7c6d-4d2f-bac3-ea3281133ad4.jpg)
![tm](https://user-images.githubusercontent.com/6567881/159117492-f3420fad-36da-4abc-a64c-03fefe8ca0d5.jpg)
