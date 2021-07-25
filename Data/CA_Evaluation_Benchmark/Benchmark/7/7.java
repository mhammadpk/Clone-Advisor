private static int [] bublesort (int[] list , int length) {

    boolean swap = true;
    int temp;

    while(swap){

        swap = false;

        for(int i = 0;i < list.length-1; i++){              
            if(list[i] > list[i+1]){
                temp = list[i];
                list[i] = list[i+1];
                list[i+1] = temp;                   
                swap = true;
            }
        }
    }
    return list;
}