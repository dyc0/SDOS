
/*
 * 4. Napisati funkciju koja učitava RGB sliku po ličnom izboru i prikazuje informacije o
 * slici. Nakon toga razdvojiti R, G i B komponente slike i prikazati sve slike istovremeno
 * u jednom prozoru. Komponentu po izboru sačuvati kao intenzitetnu sliku. Početnu RGB sliku
 * konvertovati u indeksnu, prikazati je i sačuvati kao novu sliku. Prikazati polaznu sliku
 * kao sliku u ogledalu originalne slike po proizvoljno izabranoj osi i naznačiti koja je
 * osa izabrana.
*/

#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>
// #include <libexif/exif-data.h>  // <- TODO: see how to set up cmake
// #include <libexif/exif-loader.h>

#define NUMCOLORS 12

// Namespace nullifies the use of cv::function(); 
using namespace std;
using namespace cv;

int main(){ 
    
    // Load image
    // ----------------------------
    Mat img = imread("../MrBean.jpg", IMREAD_UNCHANGED);


    // Show image
    // ----------------------------
    imshow("Original image", img);  
    waitKey(0);                       
    destroyAllWindows();
    

    // Metadata
    // ----------------------------
    // TODO: Set up for use with exif.
    std::cout << "IMAGE INFORMATION" << std::endl
              << "Dimensions: (" << img.cols << " x " << img.rows << ")" << std::endl
              << "Metadata using OpenCV here is limited. libexif can be used, but "
              << "I need to figure out how to set up cmake for it." << std::endl;


    // Color channels
    // ----------------------------
    // Showing all images in the same window is a tedious task and I shall not do it here.
    string colors[3] = {"Blue", "Green", "Red"};
    Mat bgr[3];
    split(img, bgr);
    for (int color = 0; color < 3; color++) {
        imshow(colors[color], bgr[color]);
        waitKey(0);                       
        destroyAllWindows();
        imwrite(colors[color] + ".jpg", bgr[color]);
    }


    // Indexed image
    // ----------------------------
    /*
     * TODO: Write index conversion.
    */

    return 0;
}