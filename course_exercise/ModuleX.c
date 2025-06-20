void ModuleX(int x, int y, int Wid, char* Str)
{
    unsigned  Zcode, Bcode;
    int  i, j, k, Rec, Color;
    long Len;
    char Buf[72];
    while (*Str)
    {
        if ((*Str & 0x80) && (*(Str + 1) & 0x80))
        {
            Zcode = (*Str - 0xa1) & 0x07f;
            Bcode = (*(Str + 1) - 0xa1) & 0x07f;
            Rec = Zcode * 94 + Bcode;
            Len = Rec * 72L;
            fseek(fp, Len, SEEK_SET);
            fread(Buf, 1, 72, fp);
            for (i = 0; i < 24; i++)
                for (j = 0; j < 3; j++)
                for (k = 0; k < 8; k++)
                if (Buf[i * 3 + j] >> (7 - k) & 1)
            {
                Color = y + j * 8 + k - 46;
                PutPoint(x + i, y + j * 8 + k, Color);
            }
            x = x + 24 + Wid;
            Str += 2;
        }
    }
    return;
}
