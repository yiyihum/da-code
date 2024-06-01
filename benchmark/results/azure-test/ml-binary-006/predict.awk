BEGIN {
    FS = OFS = ",";
    print "title,text,subject,date,result";
}

NR > 1 {
    # Default to true news
    result = 1;

    # Check for phrases indicating fake news
    if (tolower($2) ~ /clickbait|fake news/) {
        result = 0;
    }

    # Print the line with the result appended
    print $1, $2, $3, $4, result;
}
